<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SYS-023",
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
    "02-system/code-and-filesystem-architecture/24-repository-root-and-documentation.md",
    "02-system/code-and-filesystem-architecture/25-internal-components-node-trust-governance.md",
    "02-system/code-and-filesystem-architecture/26-internal-components-data-publication-and-knowledge.md",
    "02-system/code-and-filesystem-architecture/27-independent-subsystem-integrations.md",
    "02-system/code-and-filesystem-architecture/28-uckk-external-services-and-transport-interfaces.md",
    "02-system/code-and-filesystem-architecture/29-host-platform-files.md",
    "02-system/code-and-filesystem-architecture/30-assembly-profiles-packaging-and-release.md",
    "02-system/code-and-filesystem-architecture/31-operations-tests-tools-development-and-ci.md",
    "02-system/code-and-filesystem-architecture/32-installed-runtime-filesystem.md",
    "02-system/code-and-filesystem-architecture/33-path-ownership-and-change-rules.md"
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
    "DOC-SYS-002",
    "DOC-SYS-004",
    "DOC-SYS-007",
    "DOC-SYS-019",
    "DOC-COMP-SUBSYSTEM-BOUNDARIES",
    "DOC-DEV-000",
    "DOC-LIFE-002",
    "DOC-SEC-005",
    "DOC-OPS-000"
  ],
  "tags": [
    "code-architecture",
    "repository-architecture",
    "filesystem",
    "frozen-layout",
    "system-of-systems",
    "koa-spaces"
  ]
}
KOA:DOC-META:END -->

# Frozen Code and Filesystem Architecture

## 1. Purpose

This document freezes the source-repository architecture and installed runtime filesystem architecture of kOA-Linux Operating System. It defines the permitted top-level roots, the ownership of every structural path, the baseline file inventory, generated-output boundaries, subsystem integration boundaries, and the rules by which implementation files may be added without changing the architecture.

This series does not redesign the existing documentation corpus. It adds one architectural authority split into bounded files so that the inventory remains reviewable. The existing documentation architecture, contracts, generated indexes, and validators remain in place.

## 2. Architectural Position of kOA Spaces

kOA Spaces is the optional navigation and presentation layer. It owns the global frame, module selector, top bar, sidebar rendering, presentation routing, responsive behavior, and global-frame accessibility. It does not own the operating system, host privilege, authorization, business data, workflows, release activation, resource admission, backup authority, or subsystem state.

Inside the kOA-Linux source repository, only the kOA integration adapter, deployment descriptors, source pin, compatibility declaration, interface manifests, tests, and degradation behavior for kOA Spaces are stored. The implementation of kOA Spaces remains in its independent repository.

## 3. Frozen Repository Model

kOA-Linux SHALL use a federated system-integration repository:

- kOA-owned internal components MAY be implemented under `components/`;
- Linux host integration SHALL be implemented under `host/`;
- independent subsystem implementations SHALL NOT be copied into this repository;
- subsystem adapters, source pins, deployment declarations, and boundary tests SHALL be stored under `integrations/`;
- canonical architecture and contracts SHALL remain under `docs/`;
- profile contracts SHALL generate deployment plans rather than fork source trees;
- generated code and deployment projections SHALL be isolated under declared generated roots;
- packaging and release construction SHALL remain separate from component domain code.

## 4. Frozen Top-Level Tree

```text
koa-linux/
├── .github/
├── .koa/
├── LICENSES/
├── assembly/
├── ci/
├── components/
├── dev/
├── docs/
├── generated/
├── host/
├── integrations/
├── interfaces/
├── operations/
├── packaging/
├── profiles/
├── release/
├── tests/
├── tools/
├── .editorconfig
├── .gitattributes
├── .gitignore
├── .pre-commit-config.yaml
├── .python-version
├── .rustfmt.toml
├── Cargo.lock
├── Cargo.toml
├── CHANGELOG.md
├── CONTRIBUTING.md
├── NOTICE.md
├── README.md
├── REUSE.toml
├── SECURITY.md
├── pyproject.toml
├── rust-toolchain.toml
└── uv.lock
```

No additional top-level source directory may be introduced without changing this frozen architecture through an accepted major architecture decision.

## 5. Inventory Series

| Document | Scope |
| --- | --- |
| `24-repository-root-and-documentation.md` | Root files, repository controls, CI entrypoints, documentation boundary |
| `25-internal-components-node-trust-governance.md` | Node Agent, Identity and Trust, Resource Governor, Governance Policy Runtime |
| `26-internal-components-data-publication-and-knowledge.md` | Audit Broker, Publication Gateway, Kristal Runtime, kOA Mediatheque |
| `27-independent-subsystem-integrations.md` | Ariane, kOA Spaces, Konnaxion, Orgo, SemantiK Architect, SenTient |
| `28-uckk-external-services-and-transport-interfaces.md` | UCKK bridges, approved external surfaces, implementation transport schemas |
| `29-host-platform-files.md` | Boot, recovery, image, systemd, security, network, storage, devices, sessions |
| `30-assembly-profiles-packaging-and-release.md` | Contract-driven assembly, profile settings, packages, containers, release tooling |
| `31-operations-tests-tools-development-and-ci.md` | Operations code, test suites, developer tooling, local environments, CI policies |
| `32-installed-runtime-filesystem.md` | Installed immutable files, configuration, runtime state, persistent state, caches |
| `33-path-ownership-and-change-rules.md` | Ownership matrix, dependency rules, allowed additions, prohibited structures |

## 6. Meaning of the File Inventory

The inventory is exhaustive for the baseline structural scaffold and named implementation modules. It distinguishes three classes:

1. **Frozen structural files** — exact paths that define repository boundaries, component entrypoints, build metadata, deployment declarations, and validation controls.
2. **Registered implementation files** — source and test modules named in this series. Additional files MAY be added only inside an already admitted leaf source or test directory, must preserve the owning component boundary, and must be registered in the owning `component.toml`, `integration.toml`, or repository path-ownership file.
3. **Dynamic or generated files** — release artifacts, generated bindings, caches, receipts, database pages, media objects, and runtime state. Their roots and naming contracts are frozen, but individual instances are not source files and cannot be enumerated in advance.

The existing documentation corpus is independently inventoried by `generated/document-index.json`. This series freezes the `docs/` root, its section boundaries, and the files of this architecture series without duplicating the complete active documentation index.

## 7. Architecture Locks

- `LOCK-CODE-FS-001` — the top-level repository tree is closed.
- `LOCK-CODE-FS-002` — kOA-owned internal components and independent subsystems remain separated.
- `LOCK-CODE-FS-003` — independent subsystem implementations are never vendored into `koa-linux`.
- `LOCK-CODE-FS-004` — generated outputs never become manually maintained source authority.
- `LOCK-CODE-FS-005` — installed immutable, configurable, runtime, persistent, cache, and recovery paths remain separated.
- `LOCK-CODE-FS-006` — kOA Spaces remains navigation and presentation only.
- `LOCK-CODE-FS-007` — profiles compose shared components and do not own duplicated source trees.
- `LOCK-CODE-FS-008` — cross-component behavior uses declared interfaces rather than direct source imports or database writes.
- `LOCK-CODE-FS-009` — secrets, private keys, mutable runtime data, vendored repositories, and build outputs are prohibited from source roots.
- `LOCK-CODE-FS-010` — a change to a frozen root, ownership boundary, or runtime authority path requires an accepted major architecture decision.

## 8. Validation Expectations

A conforming implementation SHALL be able to validate:

- every committed path belongs to one declared owner;
- every top-level path is present in this architecture;
- no generated output is committed outside a declared generated location;
- no internal component imports another component's private source;
- no integration contains the implementation of its external subsystem;
- no profile creates a parallel implementation tree;
- no user-interface path reaches the privileged broker directly;
- every installed writable path belongs to one authority owner;
- kOA Spaces can be removed without removing business data or host capabilities;
- release, recovery, and last-known-good state remain distinct from active mutable component data.
