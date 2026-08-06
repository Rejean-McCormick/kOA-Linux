<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SYS-033",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "system",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/system.contract.json",
    "contracts/ai-navigation.contract.json",
    "02-system/02-logical-architecture.md",
    "02-system/04-component-boundaries.md",
    "02-system/07-cross-component-communication.md",
    "02-system/19-release-and-artifact-identity.md",
    "04-components/04-subsystem-documentation-boundaries.md",
    "05-development/00-development-model.md",
    "06-lifecycle/02-release-model.md",
    "07-security/05-privilege-boundaries.md",
    "08-operations/00-operating-model.md",
    "contracts/subsystems/koa-spaces.subsystem.json",
    "02-system/23-code-and-filesystem-architecture.md",
    "00-governance/04-change-protocol.md",
    "00-governance/09-canonical-ownership.md",
    "01-constitution/07-component-separation.md"
  ],
  "decision_ids": [],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-CODE-FS-001",
    "LOCK-CODE-FS-002",
    "LOCK-CODE-FS-003",
    "LOCK-CODE-FS-004",
    "LOCK-CODE-FS-005",
    "LOCK-CODE-FS-006",
    "LOCK-CODE-FS-007",
    "LOCK-CODE-FS-008",
    "LOCK-CODE-FS-009",
    "LOCK-CODE-FS-010"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-SYS-023",
    "DOC-GOV-004",
    "DOC-GOV-009",
    "DOC-CONST-007"
  ],
  "tags": [
    "path-ownership",
    "dependency-rules",
    "change-control",
    "naming"
  ]
}
KOA:DOC-META:END -->

# Path Ownership and Change Rules

## 1. Purpose

This document defines the rules that keep the frozen file architecture usable as implementation grows. It distinguishes an architectural change from an ordinary addition inside an admitted owner root.

## 2. Ownership Matrix

| Path | Owner | Prohibited content |
| --- | --- | --- |
| `docs/` | Documentation governance | Product source, secrets, mutable state, package payloads |
| `components/<component-id>/` | Named internal component | Another component's domain logic or migrations |
| `host/` | Host platform integration | Business workflow, application state, subsystem internals |
| `integrations/<subsystem-id>/` | kOA integration boundary | Vendored subsystem implementation or direct database mutation |
| `interfaces/` | Transport and binding maintainers | Domain-authority redefinitions |
| `assembly/` | System assembly | Component business rules or hand-maintained profile forks |
| `profiles/` | Profile implementation settings | Canonical profile definitions or copied source trees |
| `packaging/` | Packaging | Release-channel authority, signing secrets, business logic |
| `release/` | Release engineering | Mutable component state or private signing keys |
| `operations/` | Operations implementation | Canonical architecture or hidden business policy |
| `tests/` | Cross-system conformance | Production implementation used only to make tests pass |
| `tools/` | Repository tooling | Product runtime authority |
| `dev/` | Local development | Production secrets or authoritative deployment manifests |
| `ci/` | Reusable CI orchestration | Logic that cannot run locally |
| `generated/` | Generators | Manually maintained source authority |

## 3. Allowed Ordinary Additions

A new source or test file is an ordinary implementation change when all of these conditions hold:

1. it is inside an admitted leaf source, adapter, test, fixture, migration, or packaging directory;
2. its owner is already declared by `path-ownership.json`;
3. it does not introduce a new cross-component dependency;
4. it does not move authority, persistent state, privilege, or release responsibility;
5. it is registered by the owning `component.toml`, `integration.toml`, package metadata, or test manifest where applicable;
6. it passes architecture, dependency, source-pin, generated-content, runtime-path, and conformance checks.

Examples include adding a new use-case module under one component's `application/`, a new adapter behind an existing port, a new migration owned by that component, or an additional test within an existing suite.

## 4. Changes Requiring Architecture Revision

An accepted major architecture decision is required before:

- adding or renaming a top-level directory;
- moving a component between internal and external ownership;
- placing subsystem implementation code inside `koa-linux`;
- creating a shared writable database root;
- introducing a new privileged executable or broker operation class;
- adding a new immutable, configuration, persistent, recovery, or secret root outside the installed filesystem layout;
- making a generated directory manually authoritative;
- creating a profile-specific source implementation tree;
- granting kOA Spaces business, policy, resource, release, identity, or host authority;
- changing a canonical path that is referenced by release, recovery, backup, or conformance evidence.

## 5. Dependency Direction

```text
docs/contracts
      ↓ generation
generated bindings
      ↓
component domain and application
      ↓ through ports
component adapters and integration adapters
      ↓
host and assembly
      ↓
packaging and release
```

The following are prohibited:

```text
component private source → another component private source
component domain         → host, profile, package, or integration implementation
integration A            → integration B private source
kOA Spaces               → privileged broker
presentation manifest    → executable code loading
profile settings         → copied component implementation
release workflow         → undeclared live-state mutation
```

## 6. Naming Rules

- directories and non-language configuration files use `kebab-case` unless an external standard requires another name;
- Python packages use `snake_case` and remain under `src/`;
- Rust modules use `snake_case` and binaries use stable `kebab-case` executable names;
- identifiers in contracts remain stable even when public labels change;
- files named `common`, `shared`, `helpers`, `misc`, or `utils` at a broad root are prohibited unless their exact narrow responsibility is documented;
- generated files include generator and source-state metadata where the format permits it.

## 7. File Size and Splitting

A file SHALL represent one coherent responsibility. Review is mandatory when a source file exceeds 500 logical lines or a normative architecture file exceeds approximately 800 lines. A larger file is permitted only when splitting would obscure a generated table, schema, protocol, or atomic state machine. Otherwise it SHALL be split into responsibility-specific modules or a numbered documentation series.

This architecture itself is split into a series to avoid one oversized inventory file.

## 8. Prohibited Repository Content

The source repository SHALL NOT contain:

- `.git/` data inside release archives;
- private keys, production credentials, access tokens, personal secrets, or decrypted recovery material;
- runtime databases, media blobs, audit stores, backups, receipts, caches, or support bundles;
- copied Konnaxion, Orgo, Ariane, kOA Spaces, SemantiK Architect, SenTient, or UCKK repositories;
- unverified binary dependencies without source, digest, license, and provenance records;
- package manager caches, virtual environments, build directories, container layers, or generated release payloads outside declared generated paths;
- symbolic links that escape the owning repository or installed runtime root.

## 9. Validation Contract

`tools/src/koa_tools/checks/file_architecture.py` SHALL compare committed paths with the generated machine-readable lock derived from this series. The check SHALL fail on unknown top-level roots, ownerless structural files, prohibited generated content, subsystem vendoring, invalid runtime paths, private cross-component imports, or kOA Spaces authority expansion.

A successful documentation validation confirms the consistency of this series. Implementation conformance additionally requires the code-repository checks defined here once the corresponding source scaffold exists.
