<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-CONST-013",
  "document_class": "explanatory_markdown",
  "status": "active",
  "language": "en",
  "layer": "constitution",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/terminology.contract.json",
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "generated/document-index.json",
    "contracts/system.contract.json",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/artifact-classes.contract.json",
    "contracts/release-channels.contract.json",
    "contracts/integration-types.contract.json"
  ],
  "decision_ids": [
    "DEC-DOC-001",
    "DEC-DOC-002",
    "DEC-DOC-003"
  ],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-DOC-002",
    "LOCK-DOC-003",
    "LOCK-DOC-008",
    "LOCK-DOC-009",
    "LOCK-DOC-014",
    "LOCK-DOC-016",
    "LOCK-DOC-019",
    "LOCK-DOC-021",
    "LOCK-DOC-022",
    "LOCK-PROFILE-001",
    "LOCK-IMPL-001",
    "LOCK-GOV-001",
    "LOCK-GATE-001",
    "LOCK-DATA-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-GOV-001",
    "DOC-GOV-002",
    "DOC-GOV-016",
    "DOC-CONST-000",
    "DOC-CONST-001",
    "DOC-CONST-002"
  ],
  "tags": [
    "constitution",
    "glossary",
    "terminology",
    "canonical-vocabulary",
    "aliases",
    "identifiers",
    "ai-context"
  ]
}
KOA:DOC-META:END -->

# Glossary

> **Document status:** Explanatory and non-normative.  
> **Canonical authority:** `contracts/terminology.contract.json` owns canonical names, identifiers, definitions, aliases, deprecations, and controlled vocabularies. This document is a readable projection of that registry.

## 1. Purpose

This document provides the common vocabulary used across the kOA documentation corpus.

It helps readers and AI agents:

- identify the exact meaning of architectural terms;
- distinguish concepts that have related names but different authority;
- use canonical product, component, profile, artifact, release, governance, security, and development names;
- replace historical terminology during migration;
- interpret controlled vocabulary and identifier families consistently.

This document does not create independent terminology authority.

## 2. Scope

This glossary applies to all active content under `docs/`, including:

- Markdown documents;
- canonical registries and contracts;
- JSON Schemas;
- deployment profiles;
- component and artifact contracts;
- ADRs;
- requirements and alignment locks;
- generated indexes and AI context packages;
- validation messages intended for documentation users.

Historical or migration-only terminology appears only in the deprecation section.

Definitions of runtime behavior, profile membership, component responsibility, release compatibility, or artifact lifecycle remain owned by the semantic owner referenced for each term.

## 3. Canonical References

| Canonical source | Owned information |
| --- | --- |
| `contracts/terminology.contract.json` | Canonical names, identifiers, definitions, aliases, deprecations, controlled vocabularies, distinctions, and representation rules |
| `contracts/system.contract.json` | Global system behavior and boundaries |
| `generated/component-catalog.json` | Component identity, responsibility, and owned data |
| `generated/profile-catalog.json` and `contracts/profiles/*.profile.json` | Profile identity, kind, composition, and capability membership |
| `contracts/artifact-classes.contract.json` | Artifact-class meaning and lifecycle |
| `contracts/release-channels.contract.json` | Release-channel meaning and compatibility |
| `contracts/integration-types.contract.json` | External-integration identity and classification |
| `generated/decision-index.json` | Accepted choices that establish or change terminology |
| `generated/document-index.json` | Document identity, class, scope, and path |

Related governance documents include:

```text
00-governance/02-documentation-contract.md
00-governance/03-normative-language.md
00-governance/05-decision-closure-and-prohibited-ambiguity.md
00-governance/09-canonical-ownership.md
00-governance/10-interfile-alignment-locks.md
00-governance/16-language-terminology-and-style.md
```

## 4. Context

The glossary belongs to the constitutional layer because consistent vocabulary is needed across every system, profile, component, lifecycle, security, operations, and conformance document.

The glossary is machine-derived rather than independently authored. Canonical terminology changes begin in `terminology.registry.json`; this file is then regenerated.

A definition in this glossary explains a term. It does not replace the detailed contract owned by the term's semantic owner.

## 5. Conceptual Model

### 5.1 Term record

Each canonical term has:

- a stable `TERM-*` identifier;
- an exact canonical name;
- a lowercase snake-case canonical identifier;
- a category;
- a concise definition;
- a semantic owner reference;
- an explicit scope;
- alias and capitalization rules;
- a lifecycle status.

### 5.2 Name, identifier, and owner

The canonical name is the human-readable form.

The canonical identifier is the machine-readable key used in JSON, indexes, contracts, and generated references.

The semantic owner defines the detailed architectural behavior associated with the term. Terminology ownership does not transfer behavioral ownership into the glossary.

### 5.3 Alias classes

An accepted alias is a permitted shortened form that resolves to one canonical term.

A deprecated alias is retained for migration but is replaced in active prose.

A forbidden alias is rejected in active documentation because it is ambiguous, incorrectly capitalized, or collapses distinct responsibilities.

### 5.4 Unknown terms

An architectural term that cannot be resolved to a canonical entry is treated as blocked interpretation. It is not silently normalized or assigned an inferred meaning.

## 6. Canonical Glossary

The following generated tables contain every active canonical term.

<!-- GENERATED:GLOSSARY:BEGIN
source=contracts/terminology.contract.json#/terms
renderer=glossary-by-category-v1
-->
### AI Boundary

| Canonical term | Identifier | Definition | Scope | Semantic owner |
| --- | --- | --- | --- | --- |
| **approved Ariane voice adapter** | `approved_ariane_voice_adapter` | The optional approved external voice path used by Ariane without replacing local deterministic navigation. | `global` | `contracts/system.contract.json#/ai_boundary` |
| **external AI surface** | `external_ai_surface` | An optional external capability accessed through an explicit user-triggered and capability-scoped boundary. | `global` | `contracts/system.contract.json#/ai_boundary` |
| **native AI** | `native_ai` | An AI capability shipped and executed as part of the kOA baseline. | `global` | `contracts/system.contract.json#/ai_boundary` |

### Artifact Classes

| Canonical term | Identifier | Definition | Scope | Semantic owner |
| --- | --- | --- | --- | --- |
| **cultural rights policy** | `cultural_rights_policy` | A machine-readable policy governing cultural rights, consent, use, and disclosure conditions. | `global` | `contracts/artifact-classes.contract.json#/artifact_classes/cultural_rights_policy` |
| **decision receipt** | `decision_receipt` | A machine-readable record of a governed decision and its relevant inputs, outcome, and authority. | `global` | `contracts/artifact-classes.contract.json#/artifact_classes/decision_receipt` |
| **integration manifest** | `integration_manifest` | A machine-readable declaration of an external integration, its capabilities, boundaries, and configuration. | `global` | `contracts/artifact-classes.contract.json#/artifact_classes/integration_manifest` |
| **language pack** | `language_pack` | A versioned package of compiled language artifacts. | `global` | `contracts/artifact-classes.contract.json#/artifact_classes/language_pack` |
| **node profile** | `node_profile` | A machine-readable declaration of a node's selected profile, overlays, capabilities, and constraints. | `global` | `contracts/artifact-classes.contract.json#/artifact_classes/node_profile` |
| **offline bundle** | `offline_bundle` | A verified package used to transfer approved artifacts into a disconnected environment. | `global` | `contracts/artifact-classes.contract.json#/artifact_classes/offline_bundle` |
| **policy bundle** | `policy_bundle` | A versioned package of governance policy artifacts. | `global` | `contracts/artifact-classes.contract.json#/artifact_classes/policy_bundle` |
| **provenance receipt** | `provenance_receipt` | A machine-readable record of artifact origin, processing, transfer, and acceptance history. | `global` | `contracts/artifact-classes.contract.json#/artifact_classes/provenance_receipt` |
| **publication receipt** | `publication_receipt` | A machine-readable record of a publication decision and outcome. | `global` | `contracts/artifact-classes.contract.json#/artifact_classes/publication_receipt` |
| **publication request** | `publication_request` | A request submitted to the Publication Gateway for controlled cross-domain release. | `global` | `contracts/artifact-classes.contract.json#/artifact_classes/publication_request` |
| **resource envelope** | `resource_envelope` | A machine-readable declaration of CPU, memory, I/O, concurrency, queue, and process limits. | `global` | `contracts/artifact-classes.contract.json#/artifact_classes/resource_envelope` |
| **Runtime Pack** | `runtime_pack` | A versioned package consumed by a runtime component. | `global` | `contracts/artifact-classes.contract.json#/artifact_classes/runtime_pack` |
| **sovereignty bundle** | `sovereignty_bundle` | A package containing the artifacts and evidence required for a declared sovereign deployment operation. | `global` | `contracts/artifact-classes.contract.json#/artifact_classes/sovereignty_bundle` |
| **workspace port allocation** | `workspace_port_allocation` | A machine-readable allocation of host ports to one development workspace. | `global` | `contracts/artifact-classes.contract.json#/artifact_classes/workspace_port_allocation` |

### Components

| Canonical term | Identifier | Definition | Scope | Semantic owner |
| --- | --- | --- | --- | --- |
| **Ariane Runtime** | `ariane_runtime` | The local deterministic navigation and accessibility runtime for Ariane capabilities. | `global` | `generated/component-catalog.json#/components/ariane_runtime` |
| **Audit Broker** | `audit_broker` | The component that coordinates registered audit requests, evidence access, and selective disclosure. | `global` | `generated/component-catalog.json#/components/audit_broker` |
| **GF Wordbench** | `gf_wordbench` | The designated workbench for constructing and compiling language artifacts. | `global` | `generated/component-catalog.json#/components/gf_wordbench` |
| **Governance Policy Runtime** | `governance_policy_runtime` | The authority for authorization, disclosure, consent, governed privilege, and governed exceptions in profiles that deploy it. | `global` | `generated/component-catalog.json#/components/governance_policy_runtime` |
| **Identity and Trust** | `identity_and_trust` | The component authority for registered identity, trust-root, signature, and verification functions. | `global` | `generated/component-catalog.json#/components/identity_and_trust` |
| **kOA Node Agent** | `koa_node_agent` | The node-local component that performs registered node management and reporting functions. | `global` | `generated/component-catalog.json#/components/koa_node_agent` |
| **Konnaxion** | `konnaxion` | The first-class kOA domain responsible for its registered Konnaxion capabilities and authoritative data. | `global` | `generated/component-catalog.json#/components/konnaxion` |
| **Kristal Runtime** | `kristal_runtime` | The runtime that consumes and serves Kristal artifacts without becoming a universal operational database or workflow engine. | `global` | `generated/component-catalog.json#/components/kristal_runtime` |
| **Orgo** | `orgo` | The first-class kOA domain responsible for its registered Orgo capabilities and authoritative data. | `global` | `generated/component-catalog.json#/components/orgo` |
| **Publication Gateway** | `publication_gateway` | The controlled boundary for cross-domain disclosure and publication. | `global` | `generated/component-catalog.json#/components/publication_gateway` |
| **Resource Governor** | `resource_governor` | The deterministic authority for CPU, memory, I/O, concurrency, queues, scheduling, and process limits. | `global` | `generated/component-catalog.json#/components/resource_governor` |
| **SemantiK Architect Runtime** | `semantik_architect_runtime` | The runtime that executes compiled language artifacts and does not perform language construction. | `global` | `generated/component-catalog.json#/components/semantik_architect_runtime` |
| **SenTient** | `sentient` | An optional isolated research and enrichment workbench whose outputs remain candidate inputs until explicitly reviewed and imported. | `global` | `generated/component-catalog.json#/components/sentient` |
| **UCKK Publication Bridge** | `uckk_publication_bridge` | The external integration that packages and transports explicitly authorized kOA Mediatheque records to an external UCKK Moodle destination. | `global` | `generated/integration-catalog.json#/integrations/uckk_publication` |
| **kOA Mediatheque** | `koa_mediatheque` | The internal authoritative component for deterministic local media ingestion, storage, versions, metadata, rights, provenance, transformation, export, backup, and restore. | `global` | `generated/component-catalog.json#/components/koa_mediatheque` |

### Development

| Canonical term | Identifier | Definition | Scope | Semantic owner |
| --- | --- | --- | --- | --- |
| **Docker** | `docker` | A permitted OCI-compatible container runtime for the Windows/WSL development profile. | `global` | `contracts/system.contract.json#/implementation_technologies` |
| **Kubernetes** | `kubernetes` | A cluster orchestration platform permitted for selected hub, build-farm, or control-plane profiles and not required on endpoints. | `global` | `contracts/system.contract.json#/implementation_technologies` |
| **mutable dependency environment** | `mutable_dependency_environment` | An installed dependency environment whose contents can change during development and therefore cannot be shared between workspaces. | `global` | `contracts/toolchains/python-uv.toolchain.json` |
| **Podman** | `podman` | The preferred rootless container runtime for Linux development and sovereign Linux recipes. | `global` | `contracts/system.contract.json#/implementation_technologies` |
| **pyproject.toml** | `pyproject_toml` | The versioned Python project configuration file used by a workspace. | `global` | `contracts/toolchains/python-uv.toolchain.json` |
| **Quadlet** | `quadlet` | A systemd-oriented declarative mechanism used by applicable sovereign Linux recipes to manage Podman containers. | `global` | `contracts/system.contract.json#/implementation_technologies` |
| **rootless container** | `rootless_container` | A container executed without host-root privileges. | `global` | `contracts/system.contract.json#/implementation_technologies` |
| **shared content-addressed UV cache** | `shared_content_addressed_uv_cache` | A reusable download and build cache that may be shared because it does not represent a mutable installed environment. | `global` | `contracts/toolchains/python-uv.toolchain.json` |
| **UV** | `uv` | The mandatory Python dependency and environment manager for kOA development workspaces. | `global` | `contracts/toolchains/python-uv.toolchain.json` |
| **uv.lock** | `uv_lock` | The versioned UV dependency lock file used for reproducible synchronization. | `global` | `contracts/toolchains/python-uv.toolchain.json` |
| **workspace** | `workspace` | A logical development isolation unit with its own identity, mutable dependencies, services, state, ports, secrets, and resource budget. | `global` | `contracts/artifact-contracts/developer-workspace.schema.json` |
| **workspace identifier** | `workspace_id` | The stable identifier used to namespace mutable development resources. | `global` | `contracts/artifact-contracts/developer-workspace.schema.json` |
| **workspace virtual environment** | `workspace_virtual_environment` | The mutable Python virtual environment dedicated to one workspace. | `global` | `contracts/toolchains/python-uv.toolchain.json` |
| **worktree** | `worktree` | A Git checkout mechanism that may host one workspace but does not itself define the complete workspace boundary. | `global` | `contracts/artifact-contracts/developer-workspace.schema.json` |

### External Integrations

| Canonical term | Identifier | Definition | Scope | Semantic owner |
| --- | --- | --- | --- | --- |
| **ChatGPT** | `chatgpt` | An approved optional external integration surface named ChatGPT. | `global` | `contracts/integrations/chatgpt.integration.json` |
| **Gamma** | `gamma` | An approved optional external integration surface named Gamma. | `global` | `contracts/integration-types.contract.json#/integrations/gamma` |
| **Suno** | `suno` | An approved optional external integration surface named Suno. | `global` | `contracts/integration-types.contract.json#/integrations/suno` |

### Governance Concepts

| Canonical term | Identifier | Definition | Scope | Semantic owner |
| --- | --- | --- | --- | --- |
| **active authority** | `active_authority` | The set of currently activated decisions, registries, contracts, ADRs, and normative documents. | `global` | `generated/authority-manifest.json#/canonical_ownership` |
| **active documentation corpus** | `active_documentation_corpus` | The single current documentation tree under docs that participates in authority. | `global` | `contracts/terminology.contract.json#/terms` |
| **AI context package** | `ai_context_package` | A task-scoped generated projection that provides an AI agent with applicable authority, scope, requirements, locks, decisions, and prohibited assumptions. | `global` | `contracts/terminology.contract.json#/terms` |
| **Architecture Decision Record** | `architecture_decision_record` | A record of architectural context, alternatives, rationale, consequences, and decision history. | `global` | `generated/decision-index.json#/adrs` |
| **archive** | `archive` | Historical documentation retained without current product or documentation authority. | `global` | `contracts/terminology.contract.json#/terms` |
| **artifact** | `artifact` | An immutable or versioned deliverable governed by an artifact class and lifecycle contract. | `global` | `contracts/artifact-classes.contract.json#/artifact_classes` |
| **authoritative state** | `authoritative_state` | State accepted and owned by the component or registry responsible for the relevant domain. | `global` | `contracts/terminology.contract.json#/terms` |
| **Authority Registry** | `authority_registry` | The registry that activates the documentation release, registry versions, schema versions, authority order, ownership map, validation policy, and cutover state. | `global` | `generated/authority-manifest.json#/canonical_ownership` |
| **candidate input** | `candidate_input` | An external or generated result that has not yet been accepted into component-owned authoritative state. | `global` | `contracts/terminology.contract.json#/terms` |
| **canonical owner** | `canonical_owner` | The single machine-readable location authorized to define one architectural fact. | `global` | `generated/authority-manifest.json#/canonical_ownership` |
| **canonical reference** | `canonical_reference` | A repository-relative path, optionally followed by a JSON Pointer, that identifies an authoritative object. | `global` | `generated/authority-manifest.json#/canonical_ownership` |
| **canonical registry** | `canonical_registry` | A machine-readable registry with exclusive ownership of a defined architectural domain. | `global` | `generated/authority-manifest.json#/canonical_ownership` |
| **component** | `component` | A first-class architectural responsibility with explicit boundaries, owned data, interfaces, and failure behavior. | `global` | `generated/component-catalog.json#/components` |
| **deployment profile** | `deployment_profile` | A complete deployable system identity that selects and constrains the global kOA baseline for a declared purpose. | `global` | `generated/profile-catalog.json` |
| **fail-closed authority** | `fail_closed_authority` | The rule that an operation requiring authority does not proceed when identity, policy, scope, compatibility, or ownership cannot be resolved. | `global` | `generated/authority-manifest.json#/canonical_ownership` |
| **generated projection** | `generated_projection` | A reproducible view of canonical data that carries no independent authority. | `global` | `contracts/terminology.contract.json#/terms` |
| **Interfile Alignment Lock** | `interfile_alignment_lock` | A versioned machine-readable assertion that prevents mutually dependent documentation objects from drifting out of alignment. | `global` | `generated/assertion-index.json#/locks` |
| **migration evidence** | `migration_evidence` | Read-only evidence that records source lineage, disposition, redirects, and cutover history without defining current product behavior. | `global` | `contracts/terminology.contract.json#/terms` |
| **normative requirement** | `normative_requirement` | A testable obligation with a stable requirement identifier, strength, scope, owner, source decision, and validation method. | `global` | `generated/requirements-index.json#/requirements` |
| **offline continuity** | `offline_continuity` | The ability of declared core capabilities to remain available without Internet access within the applicable profile envelope. | `global` | `contracts/terminology.contract.json#/terms` |
| **owner decision** | `owner_decision` | An accepted decision that authorizes an implementation-affecting architectural fact or semantic change. | `global` | `contracts/terminology.contract.json#/terms` |
| **portability and exit** | `portability_and_exit` | The ability to export, restore, migrate, and leave a deployment without dependence on an unavailable authority or proprietary-only path. | `global` | `contracts/terminology.contract.json#/terms` |
| **profile overlay** | `profile_overlay` | A composable profile that strengthens or restricts a compatible primary profile without being independently deployable. | `global` | `generated/profile-catalog.json` |
| **recipe** | `recipe` | Non-normative implementation guidance that becomes binding only when explicitly adopted by an active profile contract. | `global` | `contracts/terminology.contract.json#/terms` |
| **recourse** | `recourse` | A defined mechanism to challenge, review, correct, or reverse a governed decision or outcome. | `global` | `contracts/terminology.contract.json#/terms` |
| **release** | `release` | A governed publication event that makes a versioned artifact or compatible artifact set available for activation. | `global` | `contracts/release-channels.contract.json` |
| **release channel** | `release_channel` | An independently versioned stream of related artifact classes. | `global` | `contracts/release-channels.contract.json` |
| **Release Set** | `release_set` | A signed or otherwise verified binding of compatible versions across the system, services, governance, and knowledge release channels. | `global` | `contracts/release-channels.contract.json` |
| **safe degradation** | `safe_degradation` | Reduction of an affected capability without silently violating authority, integrity, or unrelated core behavior. | `global` | `contracts/terminology.contract.json#/terms` |
| **selective audit** | `selective_audit` | Accountability that exposes only the evidence required for the declared audit purpose. | `global` | `contracts/terminology.contract.json#/terms` |
| **service instance** | `service_instance` | One running deployment instance of a component or component capability. | `global` | `contracts/terminology.contract.json#/terms` |

### Primary Profiles

| Canonical term | Identifier | Definition | Scope | Semantic owner |
| --- | --- | --- | --- | --- |
| **build farm** | `build_farm` | The reproducible build and artifact-production profile. | `build_farm` | `contracts/profiles/build-farm.profile.json` |
| **control plane** | `control_plane` | The profile for centralized coordination functions where those functions are explicitly deployed. | `control_plane` | `contracts/profiles/control-plane.profile.json` |
| **developer Linux workstation** | `developer_linux_workstation` | The native Linux development profile with isolated workspaces, UV-managed Python environments, and workspace-scoped services. | `developer_linux_workstation` | `contracts/profiles/developer-linux-workstation.profile.json` |
| **developer Windows/WSL workstation** | `developer_windows_wsl` | The Windows 11 and WSL2 development profile permitted for development convenience without sovereign Linux conformance. | `developer_windows_wsl` | `contracts/profiles/developer-windows-wsl.profile.json` |
| **sovereign hub** | `sovereign_hub` | A multi-service sovereign deployment profile for shared or coordinated operation. | `sovereign_hub` | `contracts/profiles/sovereign-hub.profile.json` |
| **sovereign Linux node** | `sovereign_linux_node` | The hardened Linux production profile with explicit identity, recovery, offline, privilege, and assurance controls. | `sovereign_linux_node` | `contracts/profiles/sovereign-linux-node.profile.json` |
| **user lightweight profile** | `user_lightweight` | The lightweight end-user deployment profile for local daily operation on modest hardware. | `user_lightweight` | `contracts/profiles/user-lightweight.profile.json` |

### Product Names

| Canonical term | Identifier | Definition | Scope | Semantic owner |
| --- | --- | --- | --- | --- |
| **kOA** | `koa` | The exact product-family name used in prose for the kOA ecosystem. | `global` | `contracts/system.contract.json#/identity/product_family` |
| **kOA Operating Environment** | `koa_operating_environment` | The current global operating environment that defines the common kOA system baseline. | `global` | `contracts/system.contract.json#/identity/product_name` |

### Profile Overlays

| Canonical term | Identifier | Definition | Scope | Semantic owner |
| --- | --- | --- | --- | --- |
| **appliance shell overlay** | `appliance_shell` | An overlay that constrains the user shell to a minimal appliance-oriented experience. | `appliance_shell` | `contracts/profiles/appliance-shell.profile.json` |
| **high assurance overlay** | `high_assurance` | An overlay that strengthens identity, verification, security, evidence, and operational controls. | `high_assurance` | `contracts/profiles/high-assurance.profile.json` |
| **sovereign offline overlay** | `sovereign_offline` | An overlay that requires operation and recovery within a declared disconnected environment. | `sovereign_offline` | `contracts/profiles/sovereign-offline.profile.json` |

### Release Channels

| Canonical term | Identifier | Definition | Scope | Semantic owner |
| --- | --- | --- | --- | --- |
| **governance release channel** | `governance` | The release channel for governance policies and related authoritative bundles. | `global` | `contracts/release-channels.contract.json#/channels/governance` |
| **knowledge release channel** | `knowledge` | The release channel for Kristal, language, Atlas, runtime-pack, and approved knowledge artifacts. | `global` | `contracts/release-channels.contract.json#/channels/knowledge` |
| **services release channel** | `services` | The release channel for deployable application and component service artifacts. | `global` | `contracts/release-channels.contract.json#/channels/services` |
| **system release channel** | `system` | The release channel for operating-system and system-image artifacts. | `global` | `contracts/release-channels.contract.json#/channels/system` |

### Security and Operations

| Canonical term | Identifier | Definition | Scope | Semantic owner |
| --- | --- | --- | --- | --- |
| **break-glass operation** | `break_glass_operation` | A narrowly controlled emergency operation that requires explicit authorization, evidence, and post-event review. | `global` | `contracts/system.contract.json#/security_and_operations` |
| **cross-domain publication** | `cross_domain_publication` | A controlled release of information from one authority or security domain to another. | `global` | `contracts/system.contract.json#/security_and_operations` |
| **cultural rights and consent** | `cultural_rights_and_consent` | The governance domain that constrains use, disclosure, transformation, and publication according to registered cultural rights and consent. | `global` | `contracts/system.contract.json#/security_and_operations` |
| **narrow privileged broker** | `narrow_privileged_broker` | A minimal broker that performs explicitly authorized host mutations without exposing general root access. | `global` | `contracts/system.contract.json#/security_and_operations` |
| **offline import** | `offline_import` | The controlled admission of verified artifacts into a disconnected environment. | `global` | `contracts/system.contract.json#/security_and_operations` |
| **private proof** | `private_proof` | Evidence that proves a required property without indiscriminate disclosure of underlying private information. | `global` | `contracts/system.contract.json#/security_and_operations` |
| **Software Bill of Materials** | `software_bill_of_materials` | A machine-readable inventory of software components and dependencies associated with an artifact or release. | `global` | `contracts/artifact-classes.contract.json#/artifact_classes/sbom` |
| **trust root** | `trust_root` | A configured root of trust used to validate identity, signatures, or artifact provenance within a declared scope. | `global` | `contracts/system.contract.json#/security_and_operations` |

<!-- GENERATED:GLOSSARY:END -->

## 7. Required Distinctions

Related terms remain distinct even when implementations connect them.

<!-- GENERATED:DISTINCTIONS:BEGIN
source=contracts/terminology.contract.json#/distinction_rules
renderer=terminology-distinction-table-v1
-->
| Rule | Left term | Right term | Required distinction |
| --- | --- | --- | --- |
| `TERM-DIST-001` | **Resource Governor** | **Governance Policy Runtime** | Resource control is separate from authorization, disclosure, consent, and governed privilege. |
| `TERM-DIST-002` | **Publication Gateway** | **UCKK Publication Bridge** | Publication Gateway authorizes disclosure; the bridge performs UCKK-specific packaging and transport after authorization. |
| `TERM-DIST-003` | **Ariane Runtime** | **approved Ariane voice adapter** | Local deterministic navigation is separate from the optional external voice capability. |
| `TERM-DIST-004` | **kOA Mediatheque** | **UCKK Publication Bridge** | The local Mediatheque owns local media; the bridge owns only UCKK-specific packaging and transport state. |
| `TERM-DIST-005` | **Kristal Runtime** | **GF Wordbench** | Runtime consumption is separate from language construction. |
| `TERM-DIST-006` | **SemantiK Architect Runtime** | **GF Wordbench** | Execution of compiled language artifacts is separate from language build sessions. |
| `TERM-DIST-007` | **deployment profile** | **profile overlay** | A complete deployment identity is separate from a composable strengthening or restriction. |
| `TERM-DIST-008` | **component** | **service instance** | Architectural responsibility is separate from one running instance. |
| `TERM-DIST-009` | **artifact** | **release** | A deliverable is separate from the governed event that publishes it. |
| `TERM-DIST-010` | **Release Set** | **release channel** | A compatible multi-channel version binding is separate from one independently versioned stream. |
| `TERM-DIST-011` | **workspace** | **worktree** | The complete isolation unit is separate from the Git checkout mechanism that may host it. |
| `TERM-DIST-012` | **candidate input** | **authoritative state** | An unaccepted result is separate from component-owned accepted state. |
| `TERM-DIST-013` | **recipe** | **normative requirement** | Implementation guidance is separate from a testable active obligation. |
| `TERM-DIST-014` | **owner decision** | **Architecture Decision Record** | Owner authorization is separate from the record of context, rationale, and consequences. |
<!-- GENERATED:DISTINCTIONS:END -->

These distinctions prevent a reader or AI agent from inferring shared authority, shared ownership, or substitutability from similar naming.

## 8. Aliases, Deprecated Terms, and Replacements

### 8.1 Active alias policy

<!-- GENERATED:ALIASES:BEGIN
source=contracts/terminology.contract.json#/terms
renderer=terminology-alias-table-v1
-->
| Canonical term | Accepted aliases | Deprecated aliases | Forbidden aliases |
| --- | --- | --- | --- |
| **appliance shell overlay** | `appliance shell` | None | None |
| **approved Ariane voice adapter** | None | None | `AI+Ariane` |
| **Architecture Decision Record** | `ADR` | None | None |
| **Ariane Runtime** | `Ariane` | None | None |
| **developer Windows/WSL workstation** | `Windows/WSL developer profile` | None | None |
| **Governance Policy Runtime** | None | None | `governance runtime`, `resource governor runtime` |
| **high assurance overlay** | `high assurance` | None | None |
| **kOA** | None | None | `KOA`, `Koa`, `koa` |
| **kOA Node Agent** | `Node Agent` | None | None |
| **kOA Operating Environment** | `the operating environment` | None | `kOA OS`, `KOA Operating Environment` |
| **Resource Governor** | None | None | `governance runtime`, `resource policy runtime` |
| **SemantiK Architect Runtime** | `SemantiK Runtime` | None | None |
| **Software Bill of Materials** | `SBOM` | None | None |
| **sovereign offline overlay** | `sovereign offline` | None | None |
| **UCKK Publication Bridge** | None | None | `UCKK publication bridge` |
| **kOA Mediatheque** | None | None | `Mediatheque kOA` |
| **UV** | `uv` | None | None |
<!-- GENERATED:ALIASES:END -->

### 8.2 Historical terminology

<!-- GENERATED:DEPRECATED-TERMS:BEGIN
source=contracts/terminology.contract.json#/terms
renderer=deprecated-terminology-table-v1
-->
| Historical term | Historical meaning | Replacement | Usage |
| --- | --- | --- | --- |
| **AI+Ariane** | A historical label for the external Ariane voice path. | **approved Ariane voice adapter** | Historical context only. |
| **Architect Build** | A historical umbrella term that mixed language construction and runtime execution responsibilities. | **GF Wordbench**, **SemantiK Architect Runtime** | Use GF Wordbench for language construction and SemantiK Architect Runtime for execution of compiled language artifacts. |
| **kOA Linux** | A historical name for the former Linux foundation and, in limited contexts, the Linux-specific repository. | **kOA Operating Environment**, **sovereign Linux node** | Use kOA Operating Environment for the global product and sovereign Linux node for the hardened deployment profile. |
<!-- GENERATED:DEPRECATED-TERMS:END -->

Historical terms may appear in identified migration evidence or quotations. They do not define current component, product, profile, or integration identity.

## 9. Controlled Vocabularies

The following values are closed vocabularies. A document or contract uses one of the listed values rather than inventing a synonym.

<!-- GENERATED:CONTROLLED-VOCABULARIES:BEGIN
source=contracts/terminology.contract.json#/controlled_vocabularies
renderer=controlled-vocabulary-table-v1
-->
| Vocabulary | Allowed values |
| --- | --- |
| `document_classes` | `authority`, `registry`, `schema`, `normative_markdown`, `explanatory_markdown`, `adr`, `recipe`, `generated`, `migration_evidence`, `archive`, `template` |
| `document_statuses` | `active`, `deprecated`, `superseded`, `archived` |
| `decision_statuses` | `proposed`, `accepted`, `rejected`, `deprecated`, `superseded`, `archived` |
| `registry_statuses` | `active`, `deprecated`, `superseded`, `archived` |
| `scope_kinds` | `global`, `profile`, `profile_overlay`, `component`, `artifact_class`, `development_toolchain`, `migration_only` |
| `requirement_strengths` | `SHALL`, `SHALL NOT`, `SHOULD`, `SHOULD NOT`, `MAY` |
| `validation_outcomes` | `pass`, `fail`, `blocked` |
| `semantic_change_classes` | `patch`, `minor`, `major` |
| `profile_kinds` | `primary_profile`, `profile_overlay` |
| `capability_states` | `required`, `optional`, `conditional`, `task_activated`, `excluded` |
| `activation_modes` | `always_on`, `socket_activated`, `task_activated`, `manual`, `prohibited` |
<!-- GENERATED:CONTROLLED-VOCABULARIES:END -->

### 9.1 Recognized abbreviations

<!-- GENERATED:ABBREVIATIONS:BEGIN
source=contracts/terminology.contract.json#/universally_recognized_abbreviations
renderer=abbreviation-table-v1
-->
| Abbreviation | Expanded form |
| --- | --- |
| `AI` | artificial intelligence |
| `API` | application programming interface |
| `CPU` | central processing unit |
| `I/O` | input/output |
| `JSON` | JavaScript Object Notation |
| `RAM` | random-access memory |
| `SBOM` | Software Bill of Materials |
| `SSD` | solid-state drive |
| `WSL` | Windows Subsystem for Linux |
<!-- GENERATED:ABBREVIATIONS:END -->

An abbreviation outside this table is expanded at first use unless a more specific canonical rule exists.

## 10. Representation and Identifier Rules

### 10.1 Identifier families

<!-- GENERATED:IDENTIFIER-FAMILIES:BEGIN
source=contracts/terminology.contract.json#/identifier_families
renderer=identifier-family-table-v1
-->
| Object | Pattern | Example |
| --- | --- | --- |
| `document` | `^DOC-[A-Z0-9]+(?:-[A-Z0-9]+)*-[0-9]{3}$` | `DOC-GOV-016` |
| `decision` | `^DEC-[A-Z0-9]+(?:-[A-Z0-9]+)*-[0-9]{3}$` | `DEC-DOC-003` |
| `requirement` | `^REQ-[A-Z0-9]+(?:-[A-Z0-9]+)*-[0-9]{3}$` | `REQ-DOC-LANG-001` |
| `lock` | `^LOCK-[A-Z0-9]+(?:-[A-Z0-9]+)*-[0-9]{3}$` | `LOCK-DOC-019` |
| `adr` | `^ADR-[0-9]{3}$` | `ADR-025` |
| `test` | `^TEST-[A-Z0-9]+(?:-[A-Z0-9]+)*-[0-9]{3}$` | `TEST-DOC-LANG-001` |
| `evidence` | `^EVID-[A-Z0-9]+(?:-[A-Z0-9]+)*-[0-9]{3}$` | `EVID-DOC-LANG-001` |
| `exception` | `^EXC-[A-Z0-9]+(?:-[A-Z0-9]+)*-[0-9]{3}$` | `EXC-DOC-001` |
| `term` | `^TERM-[A-Z0-9]+(?:-[A-Z0-9]+)+$` | `TERM-COMP-RESOURCE-GOVERNOR` |
<!-- GENERATED:IDENTIFIER-FAMILIES:END -->

### 10.2 Representation conventions

<!-- GENERATED:REPRESENTATION-RULES:BEGIN
source=contracts/terminology.contract.json#/representation_rules
renderer=representation-rules-table-v1
-->
| Representation | Canonical form |
| --- | --- |
| `json_keys` | `lowercase_snake_case` |
| `json_enum_values` | `lowercase_snake_case` |
| `repository_paths` | `repository_relative_forward_slash` |
| `markdown_filenames` | `lowercase_kebab_case` |
| `reserved_root_filenames` | `README.md`, `AI_CONTEXT.md`, `CHANGELOG.md` |
| `canonical_reference_format` | `<repository-relative-path>#<json-pointer>` |
| `calendar_date_format` | `YYYY-MM-DD` |
| `timestamp_format` | `RFC_3339_with_explicit_offset_or_Z` |
| `semantic_version_format` | `MAJOR.MINOR.PATCH` |
| `memory_units` | `MiB`, `GiB`, `TiB` |
| `nominal_storage_units` | `GB`, `TB` |
<!-- GENERATED:REPRESENTATION-RULES:END -->

Repository references use forward slashes and remain relative to `docs/`. JSON references use a repository-relative path followed by an optional JSON Pointer.

Product names and component names preserve their registered capitalization.

## 11. Operation Verbs and Ambiguous Phrases

### 11.1 Canonical operation verbs

<!-- GENERATED:OPERATION-VERBS:BEGIN
source=contracts/terminology.contract.json#/operation_verbs
renderer=operation-verb-table-v1
-->
| Verb | Meaning |
| --- | --- |
| **reads** | Performs non-mutating access through a declared interface. |
| **imports** | Admits content through a controlled authority boundary. |
| **publishes** | Performs controlled cross-domain release. |
| **emits** | Produces an event, receipt, or declared output. |
| **activates** | Makes a verified artifact or release current without partial authoritative state. |
| **proposes** | Creates candidate content that is not yet authoritative. |
| **accepts** | Converts validated candidate content into component-owned authoritative state. |
<!-- GENERATED:OPERATION-VERBS:END -->

### 11.2 Ambiguous operation phrases

<!-- GENERATED:AMBIGUOUS-PHRASES:BEGIN
source=contracts/terminology.contract.json#/ambiguous_operation_phrases
renderer=ambiguous-phrase-table-v1
-->
| Phrase | Policy | Precise replacements |
| --- | --- | --- |
| `shares data` | `forbidden_without_precise_operation` | `reads through API`, `publishes through gateway`, `exports artifact`, `imports verified bundle` |
| `syncs` | `forbidden_unless_contract_defines_direction_conflict_and_authority` | None |
<!-- GENERATED:AMBIGUOUS-PHRASES:END -->

A precise verb identifies direction, authority, mutation, and boundary behavior. Broad phrases do not substitute for an interaction contract.

## 12. Profile and Component Interpretation

A global term keeps the same meaning in every profile.

A profile term identifies one complete deployment identity or one composable overlay. Profile membership and capability state remain defined by profile contracts.

A component name identifies an architectural responsibility. It does not identify every process, service instance, container, database, or user interface associated with that component.

An implementation technology mentioned by a sovereign, development, appliance, or other profile remains scoped to that profile. Repetition across profiles does not change its scope.

Component aliases do not merge components. In particular:

- Resource Governor remains separate from Governance Policy Runtime;
- Publication Gateway authorizes disclosure before the UCKK Publication Bridge performs target-specific transport;
- Ariane Runtime remains separate from the approved Ariane voice adapter;
- GF Wordbench remains separate from SemantiK Architect Runtime;
- kOA Mediatheque remains authoritative for local media and separate from every external publication integration.

## 13. Failure Behavior and Safe Degradation

| Condition | Interpretation result | Continued behavior |
| --- | --- | --- |
| Unknown architectural term | `blocked` | The affected interpretation stops until a canonical term is supplied |
| Alias resolves to more than one term | `fail` | No candidate meaning is selected |
| Forbidden alias appears in active prose | `fail` | The document is corrected before activation |
| Deprecated term appears outside classified historical context | `fail` | The canonical replacement is used |
| Product or component capitalization differs from the registry | `fail` | The registered spelling is restored |
| Semantic owner reference does not resolve | `blocked` | The definition is not treated as complete authority |
| Generated glossary differs from the terminology registry | `fail` | This document is regenerated |
| Optional integration term is unavailable at runtime | Capability-specific degradation | Core terminology and non-integrated operation remain unchanged |

Terminology validation affects interpretation and documentation activation. It does not invent a fallback architectural meaning.

## 14. Security, Privacy, and Authority Considerations

Terminology can affect authority when a name selects:

- a component owner;
- a profile or overlay;
- a data or publication boundary;
- an artifact class;
- a release channel;
- an AI or external-integration surface;
- a security, audit, recourse, or cultural-rights concept.

Ambiguous terminology can incorrectly broaden access, confuse data ownership, or route work through the wrong gateway. Exact naming therefore supports least privilege, selective disclosure, correct audit attribution, and safe failure.

The glossary contains no secret, credential, user-content, or tenant-specific value.

## 15. Validation References

The terminology registry defines these validation outcomes:

```text
unknown term                 → blocked
alias collision              → fail
deprecated term in active prose → fail
forbidden alias              → fail
```

Applicable validation includes:

```bash
python docs/tools/check_language.py
python docs/tools/validate_docs.py
```

The document is valid when:

1. metadata matches `documentation.registry.json`;
2. every active registry term appears exactly once in the canonical glossary;
3. every deprecated term appears in the historical terminology table;
4. all distinction rules are reproduced;
5. all aliases and replacement references resolve to one term;
6. controlled vocabularies match the registry;
7. identifier and representation rules match the registry;
8. canonical references resolve;
9. generated blocks match their declared source;
10. active prose uses English and registered capitalization;
11. no unresolved-authority marker or placeholder appears;
12. applicable alignment locks pass.

## 16. Non-Normative Examples

### 16.1 Resource and policy control

Correct:

```text
Resource Governor limits CPU and concurrency.
Governance Policy Runtime evaluates a governed authorization request.
```

Incorrect:

```text
The governance runtime handles both resource limits and authorization.
```

The incorrect wording collapses two separate authorities.

### 16.2 UCKK publication bridge wording

Correct:

```text
UCKK Publication Bridge packages and transports explicitly authorized media to an external UCKK Moodle destination.
Publication Gateway releases approved information across a domain boundary.
```

Incorrect:

```text
The UCKK publication bridge publishes data externally.
```

The incorrect wording is ambiguous and assigns publication responsibility to the wrong gateway.

### 16.3 Historical product wording

Correct current wording:

```text
The kOA Operating Environment includes a sovereign Linux node profile.
```

Classified historical wording:

```text
The archived source used the name "kOA Linux."
```

The historical name remains evidence only.

### 16.4 Workspace and worktree

A Git worktree can host a developer workspace. The developer workspace also includes dependency, service, data, secret, port, and resource isolation; the two terms are not interchangeable.

## 17. Related Documents and Maintenance Notes

| Document | Relationship |
| --- | --- |
| `01-constitution/00-charter.md` | Establishes the constitutional context |
| `01-constitution/02-global-invariants.md` | Uses canonical terms for global invariants |
| `02-system/00-system-overview.md` | Explains the global system using this vocabulary |
| `03-profiles/00-profile-model.md` | Explains primary profiles and overlays |
| `04-components/00-component-model.md` | Explains component identity and responsibility |
| `06-lifecycle/00-artifact-model.md` | Explains artifacts, releases, activation, and recovery |
| `07-security/00-threat-model.md` | Applies authority and security terminology |
| `09-conformance/01-requirement-identification.md` | Applies controlled identifiers |

This file is regenerated after a change to canonical terminology, alias policy, controlled vocabulary, identifier family, operation verb, or distinction rule.

Changes to behavior begin in the applicable semantic owner. Changes to canonical naming begin in `contracts/terminology.contract.json`.

## Final Rule

> Canonical terminology is owned by `contracts/terminology.contract.json`. This glossary explains and projects that authority; it does not create a parallel vocabulary.
