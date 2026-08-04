<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SEC-018",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "security",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json#/offline_import_security",
    "generated/component-catalog.json",
    "contracts/components/identity-and-trust.component.json",
    "contracts/components/governance-policy-runtime.component.json",
    "contracts/components/resource-governor.component.json",
    "contracts/components/koa-node-agent.component.json",
    "contracts/components/audit-broker.component.json",
    "generated/profile-catalog.json",
    "contracts/artifact-classes.contract.json",
    "contracts/release-channels.contract.json",
    "contracts/integration-types.contract.json",
    "contracts/artifact-contracts/offline-bundle.schema.json",
    "contracts/examples/offline-bundle.example.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-SEC-001",
    "DEC-OFFLINE-001",
    "DEC-LIFE-001",
    "DEC-REL-001",
    "DEC-IMAGE-001",
    "DEC-OS-001",
    "DEC-PRIV-001",
    "DEC-DATA-001",
    "DEC-COMP-001",
    "DEC-PROFILE-001",
    "DEC-RECEIPT-001",
    "DEC-AUDIT-001",
    "DEC-PORT-001",
    "DEC-INTEGRATION-001",
    "DEC-AI-001",
    "DEC-GOV-001",
    "DEC-GATE-001"
  ],
  "requirement_ids": [
    "REQ-SEC-OFFLINE-001",
    "REQ-SEC-OFFLINE-002",
    "REQ-SEC-OFFLINE-003",
    "REQ-SEC-OFFLINE-004",
    "REQ-SEC-OFFLINE-005",
    "REQ-SEC-OFFLINE-006",
    "REQ-SEC-OFFLINE-007",
    "REQ-SEC-OFFLINE-008",
    "REQ-SEC-OFFLINE-009",
    "REQ-SEC-OFFLINE-010",
    "REQ-SEC-OFFLINE-011",
    "REQ-SEC-OFFLINE-012",
    "REQ-SEC-OFFLINE-013",
    "REQ-SEC-OFFLINE-014",
    "REQ-SEC-OFFLINE-015",
    "REQ-SEC-OFFLINE-016",
    "REQ-SEC-OFFLINE-017",
    "REQ-SEC-OFFLINE-018",
    "REQ-SEC-OFFLINE-019",
    "REQ-SEC-OFFLINE-020",
    "REQ-SEC-OFFLINE-021",
    "REQ-SEC-OFFLINE-022",
    "REQ-SEC-OFFLINE-023",
    "REQ-SEC-OFFLINE-024",
    "REQ-SEC-OFFLINE-025",
    "REQ-SEC-OFFLINE-026",
    "REQ-SEC-OFFLINE-027",
    "REQ-SEC-OFFLINE-028",
    "REQ-SEC-OFFLINE-029",
    "REQ-SEC-OFFLINE-030",
    "REQ-SEC-OFFLINE-031",
    "REQ-SEC-OFFLINE-032"
  ],
  "lock_ids": [
    "LOCK-SEC-001",
    "LOCK-SEC-002",
    "LOCK-PRIV-001",
    "LOCK-OFFLINE-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-REL-001",
    "LOCK-REL-002",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-GATE-001",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-PORT-001",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-SEC-000",
    "DOC-SEC-001",
    "DOC-SEC-002",
    "DOC-SEC-003",
    "DOC-SEC-004",
    "DOC-SEC-005",
    "DOC-SEC-006",
    "DOC-SEC-007",
    "DOC-SEC-008",
    "DOC-SEC-009",
    "DOC-SEC-010",
    "DOC-SEC-011",
    "DOC-LIFE-004",
    "DOC-LIFE-011",
    "DOC-LIFE-012",
    "DOC-LIFE-013",
    "DOC-LIFE-014",
    "DOC-LIFE-015",
    "DOC-LIFE-016",
    "DOC-SYS-001",
    "DOC-SYS-003",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-007",
    "DOC-SYS-009",
    "DOC-SYS-017",
    "DOC-SYS-019",
    "DOC-SYS-020",
    "DOC-COMP-001",
    "DOC-COMP-002",
    "DOC-PROFILE-001",
    "DOC-PROFILE-003",
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-009",
    "DOC-CONST-010",
    "DOC-CONST-011"
  ],
  "tags": [
    "security",
    "offline-import",
    "offline-bundle",
    "quarantine",
    "bounded-parsing",
    "path-traversal",
    "archive-security",
    "anti-replay",
    "revocation",
    "artifact-verification",
    "release-sets",
    "staging",
    "activation",
    "recovery",
    "receipts"
  ]
}
KOA:DOC-META:END -->

# Offline Import Security

## 1. Purpose

This document defines the global kOA security boundary for importing software, artifacts, policy, knowledge, trust material, recovery material, and controlled data across an offline boundary.

An offline transport is not trusted merely because it is physically held, sealed, labeled, previously used, or delivered by an authorized person. The transport medium, filesystem, manifest, archive structure, payload, metadata, issuer claim, audience claim, dependencies, and activation instructions are all treated as potentially hostile until independently validated.

The offline-import model is designed to prevent:

- malicious removable media;
- path traversal and unsafe extraction;
- archive expansion attacks;
- parser exhaustion;
- duplicate or ambiguous paths;
- untrusted code execution during inspection;
- replay and rollback attacks;
- revoked signer or trust-root reuse;
- cross-profile or cross-tenant delivery;
- mixed or partial Release Set activation;
- direct cross-component data mutation;
- secret exposure;
- silent online-provider substitution;
- incomplete cleanup and evidence.

Import is a transport and validation result. It is not activation.

## 2. Scope

This document applies globally to offline import of:

- Release Sets;
- system images;
- service artifacts;
- governance policy bundles;
- trust and revocation updates;
- Kristal artifacts;
- language artifacts;
- Ariane artifacts;
- UCKK-related artifacts;
- migration packages;
- test and validation packs;
- recovery runtime packs;
- component-owned backups and exports;
- provenance and evidence packages;
- operator instructions;
- recipient-encrypted payloads.

It applies to:

- removable storage;
- read-only local volumes;
- controlled physical transfer;
- isolated local mirrors;
- recovery media;
- air-gapped transfer stations;
- manually transported encrypted media.

It covers import into:

- user endpoints;
- sovereign nodes;
- sovereign hubs;
- developer and build validation environments;
- control infrastructure;
- recovery environments.

The active profile determines which bundle classes, transport classes, trust inputs, target architectures, storage limits, and recovery paths are supported.

This document does not authorize arbitrary file copying, general removable-media execution, unrestricted archive extraction, package installation, or direct loading of data into component storage.

## 3. Canonical References

| Canonical reference | Responsibility |
| --- | --- |
| `contracts/artifact-contracts/offline-bundle.schema.json` | Offline bundle structure, inventory, trust, limits, lifecycle, and evidence |
| `contracts/examples/offline-bundle.example.json` | Complete sovereign-node offline release and recovery example |
| `contracts/artifact-classes.contract.json` | Artifact-class validation, activation, rollback, retention, and profile scope |
| `contracts/release-channels.contract.json` | System, services, governance, and knowledge release identities |
| `generated/profile-catalog.json` | Profile-specific offline envelope, import capability, limits, and recovery |
| `contracts/components/identity-and-trust.component.json` | Signer, recipient, trust, certificate, revocation, and target identity |
| `contracts/components/governance-policy-runtime.component.json` | Import, emergency, exception, disclosure, and activation policy decisions |
| `contracts/components/resource-governor.component.json` | Parser, scan, extraction, decryption, testing, and staging resource admission |
| `contracts/components/koa-node-agent.component.json` | Node identity, lifecycle state, target health, and recovery readiness |
| `contracts/components/audit-broker.component.json` | Critical import and activation evidence routing |
| `generated/component-catalog.json` | Component identities and authoritative data ownership |
| `contracts/integration-types.contract.json` | Optional remote providers and capability-scoped failure |
| `contracts/system.contract.json#/offline_import_security` | Global import states and security model |
| `generated/requirements-index.json` | Normative offline-import requirements |
| `generated/assertion-index.json` | Security, offline, lifecycle, release, profile, component, data, and AI assertions |
| `generated/traceability.json` | Bundle, artifact, decision, test, evidence, profile, and lifecycle relationships |
| `generated/exception-index.json` | Bounded import exceptions and compensating controls |
| `generated/test-catalog.json` | Malicious media, parser, replay, compatibility, lifecycle, and cleanup tests |
| `generated/evidence-catalog.json` | Import, failure, staging, activation, and recovery evidence |

The adjacent lifecycle and security documents are:

```text
06-lifecycle/04-release-sets.md
06-lifecycle/11-offline-bundles.md
06-lifecycle/12-artifact-verification.md
06-lifecycle/13-activation-and-verification.md
06-lifecycle/14-recovery.md
06-lifecycle/15-data-schema-evolution.md
06-lifecycle/16-forward-repair.md
07-security/03-identity-trust-and-signatures.md
07-security/04-trust-root-scoping.md
07-security/05-privilege-boundaries.md
07-security/06-privileged-broker.md
07-security/07-secrets-and-keys.md
07-security/19-software-supply-chain.md
07-security/20-break-glass-security.md
```

## 4. Threat, Trust, and State Model

### 4.1 Untrusted transport model

The importer assumes that an offline medium can contain:

- a malicious filesystem;
- misleading labels;
- malformed manifests;
- oversized records;
- deceptive Unicode or case-colliding names;
- paths targeting locations outside quarantine;
- links to host files;
- device or socket entries;
- compressed expansion attacks;
- nested archives;
- duplicate path entries;
- revoked artifacts;
- stale trust material;
- wrong-recipient encrypted payloads;
- incompatible but individually valid artifacts;
- instructions intended to trigger unsafe operator actions.

Physical custody does not replace cryptographic or semantic validation.

### 4.2 Security states

| State | Meaning |
| --- | --- |
| `media_detected` | A transport is present but no content is trusted |
| `media_identified` | Medium identity and handling class are recorded |
| `quarantined` | Candidate content is isolated from active namespaces |
| `manifest_parsed` | Bounded inert parsing completed |
| `authority_validated` | Issuer, audience, trust, validity, sequence, and revocation checks passed |
| `inventory_validated` | Paths, sizes, classes, dependencies, and signatures passed |
| `compatibility_validated` | Profile, Release Set, component, schema, and recovery compatibility passed |
| `import_validated` | Local tests passed and an import receipt can be issued |
| `imported` | Eligible material exists in controlled inactive storage |
| `staged` | Lifecycle owner prepared declared inactive artifacts or migration inputs |
| `activation_pending` | Separate activation authority and checks are required |
| `rejected` | Candidate cannot proceed |
| `quarantine_hold` | Material is retained for investigation |
| `disposed` | Quarantined and temporary material received an authorized final disposition |

Only lifecycle contracts can move imported material into an active state.

### 4.3 Bundle identity

A bundle identity is defined by its signed manifest and declared version.

The manifest identifies:

- issuer;
- audience;
- target;
- profile;
- sequence;
- validity;
- purpose;
- source and target Release Sets;
- channel releases;
- artifact inventory;
- dependencies;
- parser and extraction limits;
- trust inputs;
- migration plan;
- import plan;
- activation plan;
- recovery plan;
- tests;
- evidence;
- signatures.

A filename or media label is not the bundle identity.

### 4.4 Trust sources

Offline verification uses locally retained:

- trusted issuer identities;
- trust roots;
- signer scopes;
- revocation state;
- withdrawal state;
- profile contracts;
- artifact-class contracts;
- release-channel manifests;
- supported schema versions;
- last imported sequence;
- last active Release Set;
- applicable policy;
- recovery candidates.

A bundle cannot redefine the trust used to validate itself unless an independently trusted transition contract explicitly permits a trust update and validates its predecessor relationship.

### 4.5 Anti-replay and rollback protection

The importer tracks sequence by declared bundle series, audience, trust domain, or target scope.

A duplicate import returns the prior result when the same idempotency identity is valid.

A lower or equal sequence after successful import is rejected unless a separately authorized recovery contract identifies the exact permitted rollback or replay purpose.

Release rollback remains a lifecycle transition and cannot be smuggled through an older offline bundle.

### 4.6 Clock-degraded validation

Offline targets can have uncertain time.

The bundle declares clock assumptions and maximum uncertainty.

When time confidence is insufficient, the importer relies on retained sequence, predecessor, revocation, issue, support, and local authority state and enters the declared review or restricted path.

Time uncertainty does not extend validity automatically.

### 4.7 Parser and extraction boundary

The parser consumes only the minimal manifest representation needed for validation.

The extractor writes only to a newly allocated quarantine root.

The importer enforces:

- path normalization;
- one canonical path per entry;
- no absolute paths;
- no parent-directory segments;
- no links;
- no device or socket entries;
- no nested archives;
- bounded decompression;
- bounded file counts;
- bounded sizes;
- bounded directory depth;
- bounded parser memory and time;
- inert handling of optional metadata.

No payload-supplied hook, script, plugin, codec, installer, macro, or handler runs during this phase.

### 4.8 Encryption boundary

Recipient encryption protects confidentiality but does not establish authority.

Issuer, target, audience, sequence, trust, and manifest validation precede decryption.

Decrypted content remains quarantined.

Temporary decryption keys and plaintext copies follow the secret-handling and cleanup contracts.

### 4.9 Artifact and Release Set boundary

Each artifact is validated under its artifact class.

A release bundle selecting one changed channel still names all four channels and proves the complete resulting Release Set.

A valid artifact can remain incompatible with the target set.

### 4.10 Data ownership boundary

An offline importer owns quarantine and import state only.

It does not own component data.

Backups, exports, migrations, and data packages are passed to the owning component for staging, validation, restore, or migration.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-SEC-OFFLINE-001,REQ-SEC-OFFLINE-002,REQ-SEC-OFFLINE-003,REQ-SEC-OFFLINE-004,REQ-SEC-OFFLINE-005,REQ-SEC-OFFLINE-006,REQ-SEC-OFFLINE-007,REQ-SEC-OFFLINE-008,REQ-SEC-OFFLINE-009,REQ-SEC-OFFLINE-010,REQ-SEC-OFFLINE-011,REQ-SEC-OFFLINE-012,REQ-SEC-OFFLINE-013,REQ-SEC-OFFLINE-014,REQ-SEC-OFFLINE-015,REQ-SEC-OFFLINE-016,REQ-SEC-OFFLINE-017,REQ-SEC-OFFLINE-018,REQ-SEC-OFFLINE-019,REQ-SEC-OFFLINE-020,REQ-SEC-OFFLINE-021,REQ-SEC-OFFLINE-022,REQ-SEC-OFFLINE-023,REQ-SEC-OFFLINE-024,REQ-SEC-OFFLINE-025,REQ-SEC-OFFLINE-026,REQ-SEC-OFFLINE-027,REQ-SEC-OFFLINE-028,REQ-SEC-OFFLINE-029,REQ-SEC-OFFLINE-030,REQ-SEC-OFFLINE-031,REQ-SEC-OFFLINE-032 -->
- **REQ-SEC-OFFLINE-001 — SHALL:** Every offline import identify the transport medium, bundle identity, bundle class, issuer, intended audience, target, sequence, validity interval, source Release Set where applicable, and requested import purpose before any payload is staged.
- **REQ-SEC-OFFLINE-002 — SHALL:** Offline media and bundle contents be treated as untrusted until bounded parsing, authority, signature, scope, sequence, revocation, compatibility, and artifact validation all pass.
- **REQ-SEC-OFFLINE-003 — SHALL:** The import path copy or expose the candidate through an isolated quarantine that is not an executable search path, ordinary component storage namespace, active artifact location, or user-authoritative data location.
- **REQ-SEC-OFFLINE-004 — SHALL NOT:** An importer execute, load as code, mount with execution enabled, start, activate, migrate, decrypt into an active namespace, or otherwise trust payload content before the validation phase authorizes that operation.
- **REQ-SEC-OFFLINE-005 — SHALL:** Manifest parsing enforce declared limits for manifest size, inventory entries, total payload size, individual payload size, directory depth, filename length, compression expansion, and parser resource use.
- **REQ-SEC-OFFLINE-006 — SHALL NOT:** Offline import accept absolute paths, parent-directory traversal, duplicate paths, symbolic links, hard links, device files, sockets, named pipes, archive nesting, or filesystem metadata that redirects extraction outside quarantine.
- **REQ-SEC-OFFLINE-007 — SHALL:** Unknown required fields, unknown required artifact classes, unsupported manifest versions, and ambiguous parsing produce rejection; unknown optional metadata remain inert and never trigger execution.
- **REQ-SEC-OFFLINE-008 — SHALL:** Bundle authority validation verify the manifest signer, signer scope, issuer status, intended audience, target profile, target trust domain, validity, withdrawal, and revocation using locally available trusted state.
- **REQ-SEC-OFFLINE-009 — SHALL:** Every imported artifact resolve through a declared inventory entry, artifact class, version, release channel, dependency set, activation role, producer authority, and artifact signature.
- **REQ-SEC-OFFLINE-010 — SHALL NOT:** The presence of a filename, directory, package label, transport-medium label, prior local copy, ordinary file digest list, or successful extraction establish artifact or bundle authority.
- **REQ-SEC-OFFLINE-011 — SHALL:** Recipient-encrypted material be decrypted only after issuer, audience, target, sequence, and trust validation and only into isolated temporary storage controlled by the intended recipient authority.
- **REQ-SEC-OFFLINE-012 — SHALL NOT:** Offline bundles contain unrestricted private signing keys, ordinary component credentials, general host-administration secrets, user passwords, recovery secrets outside their declared recovery class, or credentials for undeclared recipients.
- **REQ-SEC-OFFLINE-013 — SHALL:** Offline import enforce monotonic sequence, duplicate-import idempotency, replay protection, predecessor or source-set compatibility, and explicit behavior for clock-degraded targets.
- **REQ-SEC-OFFLINE-014 — SHALL NOT:** Clock degradation, network absence, stale online status, prior successful import, or media custody extend validity, suppress revocation, lower sequence requirements, or convert an unknown authority state into approval.
- **REQ-SEC-OFFLINE-015 — SHALL:** A Release Set bundle identify and validate explicit system, services, governance, and knowledge release identities and the complete transitive compatibility of the resulting target composition.
- **REQ-SEC-OFFLINE-016 — SHALL NOT:** A complete or partial channel import become active unless the resulting four-channel Release Set, profile composition, artifacts, migrations, policies, knowledge, offline envelope, and recovery path pass local validation.
- **REQ-SEC-OFFLINE-017 — SHALL:** Import, staging, migration, activation, rollback, restore, and recovery remain separate lifecycle transitions with distinct authority, state, failure behavior, and receipts.
- **REQ-SEC-OFFLINE-018 — SHALL NOT:** Successful media detection, quarantine copy, parsing, decryption, signature verification, import, extraction, artifact staging, migration preparation, service restart, or system reboot be reported as completed activation.
- **REQ-SEC-OFFLINE-019 — SHALL:** Component-owned migrations and data imports execute through the owning component's contracts and identities and preserve component ownership, schema, validation, retry, recovery, and evidence boundaries.
- **REQ-SEC-OFFLINE-020 — SHALL NOT:** An offline importer, recovery coordinator, privileged broker, archive tool, installer, or lifecycle coordinator directly write across participant component authoritative stores.
- **REQ-SEC-OFFLINE-021 — SHALL:** The importer validate available storage, quarantine capacity, decryption capacity, temporary-space bounds, resource reserves, and evidence buffering before accepting or expanding payload content.
- **REQ-SEC-OFFLINE-022 — SHALL:** Resource-intensive parsing, scanning, extraction, decryption, migration testing, and artifact verification use Resource Governor limits without granting Resource Governor import, artifact, policy, data, or activation authority.
- **REQ-SEC-OFFLINE-023 — SHALL:** Governed offline import decisions use Governance Policy Runtime where required and record allow, deny, or review outcomes without allowing policy evaluation to replace technical verification.
- **REQ-SEC-OFFLINE-024 — SHALL:** Optional external integrations, AI services, remote registries, online reputation systems, and remote verification services remain unnecessary for locally declared offline import, validation, activation, rollback, and recovery.
- **REQ-SEC-OFFLINE-025 — SHALL NOT:** Unavailable remote verification authorize silent provider substitution, external AI analysis of sensitive bundle content, skipped local checks, broader privilege, or direct network execution of imported material.
- **REQ-SEC-OFFLINE-026 — SHALL:** A validation or import failure leave the active Release Set and authoritative component state unchanged, retain minimized failure evidence, remove decrypted temporary material as declared, and keep unsafe material quarantined or destroy it through an authorized procedure.
- **REQ-SEC-OFFLINE-027 — SHALL:** A successful import produce an idempotent machine-readable receipt identifying media, bundle, issuer, audience, target, sequence, source and target Release Sets, inventory result, validation result, actor, authority, and evidence.
- **REQ-SEC-OFFLINE-028 — SHALL:** Critical staging, migration, activation, rollback, recovery, trust update, revocation update, and quarantine-disposition transitions produce separate machine-readable receipts or evidence records.
- **REQ-SEC-OFFLINE-029 — SHALL:** Offline import logs, errors, receipts, diagnostics, and evidence minimize governed payload content, omit secret material, preserve stable identifiers and reason codes, and support selective disclosure.
- **REQ-SEC-OFFLINE-030 — SHALL:** After success or terminal failure, cleanup unmount transport media, close parser and decryption contexts, remove temporary executable permissions, remove decrypted temporary material, revoke temporary access, and verify quarantine disposition.
- **REQ-SEC-OFFLINE-031 — SHALL:** Offline import procedures, parsers, quarantine controls, trust inputs, bundles, recovery candidates, and replay defenses be tested at the profile-declared cadence and after semantic changes that affect their validity.
- **REQ-SEC-OFFLINE-032 — SHALL:** Offline-import-security conformance pass only when media, quarantine, parser limits, path controls, authority, signatures, revocation, replay, encryption, compatibility, migration, lifecycle separation, offline, cleanup, receipts, and negative-malicious-input tests all pass.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Secure Offline Import Procedure

### 6.1 Prepare the target

Before accepting media, the target resolves:

1. target identity;
2. active profile composition;
3. active Release Set;
4. import authority;
5. supported transport and bundle classes;
6. quarantine capacity;
7. parser and extraction limits;
8. locally trusted issuers and revocation state;
9. evidence buffering;
10. recovery readiness.

The target enters an import-specific state without changing ordinary active authority.

### 6.2 Identify transport media

The operator or device service records:

- medium identity;
- transport class;
- physical custody or delivery record;
- write-protection state;
- connection time;
- target;
- initiating actor;
- intended bundle.

Automount and automatic execution remain disabled.

The source is read through the profile-approved import path.

### 6.3 Create quarantine

The importer creates a fresh isolated quarantine root with:

- a unique import identity;
- no execution permission;
- no ordinary service discovery;
- no active component data path;
- no active artifact path;
- bounded storage allocation;
- controlled ownership;
- cleanup and evidence rules.

The source can be copied to quarantine or read through an equally isolated bounded interface.

### 6.4 Parse the manifest

The importer reads only the declared manifest entry.

Before allocating payload-sized resources, it validates:

- manifest size;
- syntax;
- schema version;
- required fields;
- unique identifiers;
- inventory count;
- declared parser limits;
- bundle class;
- target and purpose.

Malformed, ambiguous, duplicate, unsupported, or oversized manifests are rejected.

### 6.5 Validate authority and scope

Identity and Trust or the profile-declared verifier checks:

- manifest signature;
- signer identity;
- signer role and scope;
- issuer validity;
- intended audience;
- target identity;
- target profile;
- trust domain;
- validity interval;
- revocation;
- withdrawal;
- sequence;
- predecessor relationship;
- recovery-specific authority when applicable.

A trust update inside the same bundle is not used to validate the bundle's original authority.

### 6.6 Validate inventory structure

Before extraction, the importer validates each inventory entry:

- path;
- canonical uniqueness;
- declared size;
- artifact identity;
- artifact class;
- release channel;
- version;
- required or optional status;
- activation role;
- owner component where applicable;
- schema;
- dependencies;
- signature reference.

Dependency cycles or missing required entries reject the candidate.

### 6.7 Enforce path and archive controls

The extraction planner rejects:

- absolute paths;
- parent-directory traversal;
- alternate path separators that escape quarantine;
- case or normalization collisions;
- duplicate paths;
- links;
- device entries;
- sockets and named pipes;
- special filesystem metadata;
- archives inside archives;
- undeclared compression;
- expansion beyond declared limits.

Directories and files are created with inert permissions.

### 6.8 Decrypt recipient material

After authority and inventory validation, recipient-scoped material can be decrypted.

The intended recipient authority verifies the envelope and releases only the key operation needed for this import.

Plaintext enters isolated temporary storage under the same size, path, and execution controls.

### 6.9 Verify artifacts

Each artifact verifier checks:

- producer signature;
- signer authority and revocation;
- artifact identity;
- artifact class;
- version;
- target architecture;
- profile applicability;
- schema;
- dependencies;
- release-channel relationship;
- withdrawal state;
- class-specific negative tests.

A bundle-level signature does not replace artifact-level validation.

### 6.10 Validate complete compatibility

For Release Set material, the target evaluates:

1. all four channel identities;
2. profile and overlays;
3. architecture and operating system;
4. component versions;
5. interfaces and events;
6. schemas and migration paths;
7. governance policy compatibility;
8. knowledge runtime compatibility;
9. offline envelope;
10. integrations;
11. rollback, restore, and recovery;
12. required evidence.

A blocked required validator blocks the bundle.

### 6.11 Run local security and conformance tests

The validation pack runs locally and can include:

- malicious path tests;
- decompression-limit tests;
- schema tests;
- signature and revoked-signer tests;
- audience and profile mismatch tests;
- replay and sequence tests;
- wrong-recipient tests;
- incomplete inventory tests;
- migration preflight;
- offline-capability tests;
- recovery-readiness tests;
- lifecycle separation tests.

Tests execute in isolated contexts and do not activate the candidate.

### 6.12 Issue the import result

A passing candidate receives an import receipt.

The receipt states that eligible material is available for inactive staging.

A failing candidate receives reason codes and quarantine disposition.

The active Release Set and component stores remain unchanged.

### 6.13 Stage through lifecycle contracts

A separate lifecycle action can:

- write an inactive system slot;
- stage service artifacts;
- load an inactive policy bundle;
- load inactive knowledge artifacts;
- prepare component-owned migrations;
- prepare trust or revocation transitions;
- prepare recovery material.

Staging uses artifact and component contracts.

### 6.14 Activate separately

Activation resolves fresh authority and revalidates target state.

It checks that the import receipt remains applicable, no signer or artifact has been revoked, sequence and validity remain acceptable, resources and recovery remain available, and migrations and health gates can complete.

Only the complete declared lifecycle transition changes active authority.

### 6.15 Clean up

After import, rejection, staging, or terminal failure, the procedure:

1. closes source and parser handles;
2. unmounts transport media;
3. removes decrypted temporary material;
4. removes temporary credentials and authority;
5. removes execution permissions;
6. retains or destroys quarantine according to disposition;
7. preserves minimized evidence;
8. records cleanup completion.

## 7. Failure States and Safe Degradation

| Failure condition | Required behavior | Retained capability | Prohibited behavior | Evidence |
| --- | --- | --- | --- | --- |
| Media identity is unavailable | Reject or hold for authorized investigation | Current active system | Guessing bundle custody | Media result |
| Automount or execution is triggered | Stop import, isolate the target, and investigate | Unaffected active authority | Continuing validation in the same unsafe context | Import incident |
| Manifest exceeds limits | Reject before payload expansion | Current active system | Increasing limits from bundle metadata alone | Parser result |
| Manifest is ambiguous or unsupported | Reject | Other supported bundles | Selecting a convenient interpretation | Schema result |
| Path traversal or special entry is present | Reject the bundle and retain evidence | Current active system | Sanitizing silently and continuing | Extraction result |
| Expansion ratio or total size exceeds limits | Stop extraction and clean temporary state | Parsed manifest and evidence | Continuing until storage exhaustion | Resource result |
| Signature is invalid | Reject | Existing trusted releases | Using physical custody as authority | Signature result |
| Signer is revoked or out of scope | Reject | Other valid signers | Accepting because the signature is mathematically valid | Authority result |
| Intended audience or target does not match | Reject | Correctly scoped imports | Re-targeting the bundle locally | Audience result |
| Sequence is stale or replayed | Return prior receipt or reject according to contract | Current imported and active state | Reimporting to force rollback | Replay result |
| Clock confidence is inadequate | Enter declared review or restricted validation | Sequence and local trust checks | Extending validity implicitly | Clock result |
| Recipient decryption fails | Keep encrypted material quarantined | Non-encrypted valid entries where independent | Trying other recipients or providers | Decryption result |
| Artifact signature or class validation fails | Reject the affected required bundle | Current active artifacts | Partial activation of the remaining required entries | Artifact result |
| One channel is missing | Reject the Release Set bundle | Current active set | Keeping an unnamed installed channel | Release result |
| Compatibility is blocked | Keep candidate inactive | Current active set | Assuming compatibility | Compatibility result |
| Migration preflight fails | Keep data and candidate inactive | Current component authority | Directly loading restored or migrated state | Migration result |
| Evidence buffering is unavailable | Block critical import or staging completion | Read-only inspection | Unevidenced lifecycle transition | Evidence result |
| Resource reserve is insufficient | Pause or reject before expansion or staging | Current active operation | Consuming recovery reserve | Capacity result |
| Remote verifier is unavailable | Continue with declared local verification or reject the dependent capability | Local core validation | Silent online-provider substitution | Offline result |
| Cleanup cannot be verified | Keep import state open or restricted | Evidence and current active authority | Reporting final success | Cleanup result |

Safe degradation leaves the current active authority unchanged and contains the candidate. It does not weaken trust, broaden scope, skip revocation, execute imported code, or create an unofficial active state.

## 8. Cross-Component Interactions

### 8.1 Identity and Trust

Identity and Trust validates:

- issuer;
- signer;
- recipient;
- target;
- trust domain;
- certificates;
- validity;
- revocation;
- sequence authority;
- recovery authority.

It can release recipient-scoped decryption operations without exposing general private key material.

### 8.2 Governance Policy Runtime

Governance Policy Runtime evaluates governed import, emergency, trust-update, recovery, and activation requests where the profile requires it.

The policy result does not validate signatures, parse archives, or activate artifacts.

### 8.3 Resource Governor

Resource Governor limits parser memory, decompression, storage, scanner concurrency, migration tests, and staging work.

It cannot approve an import or delete component-owned data to make room.

### 8.4 kOA Node Agent and privileged broker

kOA Node Agent exposes target identity, active Release Set, profile, storage state, and recovery readiness.

The privileged broker performs narrow host operations such as writing an inactive system slot or switching an authorized boot target.

It does not expose a general shell or arbitrary imported-script execution path.

### 8.5 Artifact and release owners

Each artifact-class owner validates its own artifact.

Release-channel owners publish channel manifests.

The lifecycle owner assembles and activates the complete Release Set.

The importer coordinates validation without replacing these owners.

### 8.6 Component owners

A component owner receives its migration, restore, or data package only after bundle and artifact validation.

The component independently validates the package and stages its own state.

### 8.7 Audit Broker

Audit Broker records:

- media receipt;
- import authority;
- validation;
- rejection;
- quarantine disposition;
- staging;
- migration;
- activation;
- rollback;
- recovery;
- cleanup.

Evidence excludes unrestricted payload content and secret values.

### 8.8 Publication Gateway and UCKK Dimension Gateway

Offline media admission into UCKK remains governed by UCKK Dimension Gateway and UCKK Platform contracts.

Governed publication remains controlled by Publication Gateway.

The generic offline importer does not merge these boundaries.

### 8.9 External integrations and AI

External verification and AI assistance are optional and absent from the required offline path.

Sensitive bundle content is not sent to external AI for classification or diagnosis.

No AI result establishes trust, compatibility, or activation authority.

### 8.10 Recovery environment

A recovery environment can use the same secure import stages for a recovery bundle.

Recovery-specific authority, source compatibility, restricted operation, and post-event review remain required.

## 9. Decision Closure and Prohibited Assumptions

This document is supported by the accepted decisions declared in its metadata.

A semantic change to offline-import security requires:

1. an accepted owner decision;
2. impact analysis across profiles, parsers, transport media, trust, artifacts, Release Sets, components, migrations, secrets, offline behavior, recovery, evidence, tests, and operations;
3. canonical contract updates;
4. complete validation before activation.

The following assumptions are prohibited:

- physical custody proves authenticity;
- sealed packaging proves payload safety;
- read-only media contains only safe files;
- a familiar filename identifies the artifact;
- successful extraction proves validity;
- one bundle signature validates every artifact automatically;
- a per-file digest inventory proves release authority;
- an old trusted signer remains currently authorized;
- an online status service is required for offline verification;
- absence of online revocation data means not revoked;
- an uncertain clock extends validity;
- the operator can override audience or profile mismatch;
- a lower sequence is acceptable for troubleshooting;
- a duplicate import can rerun mutations;
- quarantine can share an active application or component data path;
- mounted media can be executable during inspection;
- archive paths can be sanitized silently;
- links are harmless inside quarantine;
- nested archives are acceptable when the outer archive is signed;
- unknown metadata can trigger optional plugins;
- decryption proves sender authority;
- imported material can be staged directly into active locations;
- import success means activation success;
- a system reboot proves Release Set activation;
- one valid channel can be activated while another remains implicit;
- a lifecycle coordinator can write component stores directly;
- unavailable remote verification permits skipping local checks;
- external AI can safely inspect sensitive imported content;
- cleanup is complete when the medium is unplugged;
- source-code behavior can bypass the active import contract.

No active exception currently weakens a requirement in this document.

## 10. Validation Criteria

This document is conformant when:

1. it is registered as `DOC-SEC-018`, active, English, and globally scoped;
2. every canonical reference resolves or is present in the planned canonical inventory;
3. every declared decision is accepted;
4. every requirement is unique, active, and testable;
5. every lock exists when the canonical lock registry is active and applicable assertions pass;
6. every import identifies media, bundle, issuer, audience, target, sequence, purpose, and Release Set context;
7. media and payload remain untrusted before complete validation;
8. quarantine is isolated from execution, active artifacts, and component data;
9. parser and extraction limits are bounded and profile-compatible;
10. absolute paths, traversal, links, duplicate paths, special files, and nested archives are rejected;
11. unknown required semantics reject and optional metadata remains inert;
12. signer, issuer, audience, target, validity, withdrawal, and revocation tests pass locally;
13. recipient decryption occurs only after authority validation;
14. unrestricted private and operational credentials are absent;
15. sequence, replay, predecessor, duplicate, and clock-degraded tests pass;
16. every inventory entry has a valid artifact identity, class, version, dependency, role, and signature;
17. all four Release Set channels are explicit and transitively compatible;
18. import, staging, migration, activation, rollback, restore, and recovery remain separate;
19. component-owned migrations and data imports preserve ownership;
20. capacity validation protects active and recovery reserves;
21. Governance Policy Runtime and Resource Governor remain separate from technical trust and lifecycle authority;
22. required offline validation works without remote providers or AI;
23. failure leaves active authority unchanged and contains unsafe material;
24. import and critical lifecycle receipts are complete and idempotent;
25. logs and evidence minimize payload and secret content;
26. cleanup removes temporary decryption state, access, execution permissions, and mounts;
27. malicious media, malformed manifest, parser-exhaustion, archive, replay, wrong-recipient, revoked-signer, incomplete-set, and mixed-state tests pass;
28. recovery imports preserve recovery authority and restricted-mode behavior;
29. test cadence and semantic-change retesting remain current;
30. no undeclared provider substitution or direct imported-script execution path exists;
31. no unresolved marker, implicit authority, or partial activation claim exists;
32. the active text contains the complete required section structure.

Applicable failure codes include:

```text
offline_media_identity_missing
offline_automount_execution_detected
offline_quarantine_isolation_failed
offline_manifest_too_large
offline_manifest_unsupported
offline_manifest_ambiguous
offline_inventory_limit_exceeded
offline_payload_size_limit_exceeded
offline_compression_limit_exceeded
offline_path_traversal_detected
offline_duplicate_path_detected
offline_link_entry_detected
offline_special_file_detected
offline_nested_archive_detected
offline_bundle_signature_invalid
offline_bundle_authority_invalid
offline_bundle_audience_mismatch
offline_bundle_target_mismatch
offline_bundle_sequence_stale
offline_bundle_replay_detected
offline_clock_confidence_insufficient
offline_recipient_decryption_failed
offline_artifact_signature_invalid
offline_artifact_class_invalid
offline_release_channel_missing
offline_release_set_incompatible
offline_component_owner_bypass
offline_import_activation_collision
offline_evidence_path_unavailable
offline_cleanup_incomplete
```

A required validator that cannot run produces `blocked`, not `pass`.

## 11. Non-Normative Examples

### Example 1 — Valid sovereign release bundle

An operator inserts a read-only medium containing a sovereign-node release bundle.

The node records the medium, copies the candidate into non-executable quarantine, parses the bounded manifest, validates issuer, audience, sequence, revocation, all four channels, artifacts, migrations, offline capability, and recovery readiness, then issues an import receipt. The active Release Set remains unchanged until a separate activation.

### Example 2 — Path traversal attack

A signed-looking archive contains an entry named with parent-directory segments targeting a system configuration location.

The importer rejects the complete bundle before extraction. It does not rewrite the path and continue. The failure receipt identifies the offending inventory entry without exposing unrelated payload content.

### Example 3 — Compression expansion attack

A bundle declares a small compressed file whose expansion would exceed the profile's ratio and storage limits.

The extraction planner rejects it before consuming recovery storage. The current active set and component stores remain unchanged.

### Example 4 — Revoked signer

A previously trusted release signer was revoked after a bundle was produced.

The offline node imports a current revocation update through an independently valid trust path. The older bundle's mathematical signature remains verifiable, but its signer is no longer authorized, so activation is rejected.

### Example 5 — Wrong recipient

A bundle contains recipient-encrypted recovery material intended for another trust domain.

Audience and recipient validation fail before decryption. The importer does not try alternate local keys and does not expose the encrypted payload to an external service.

### Example 6 — Stale sequence

A medium contains a bundle with sequence 23 after sequence 24 was already imported successfully.

The importer rejects it as stale. A rollback to the older Release Set can occur only through a separately authorized rollback or recovery procedure that validates current data compatibility.

### Example 7 — Component backup

An offline bundle contains an Orgo backup and migration package.

The generic importer validates the bundle and artifact identities, then passes the staged package to Orgo's restore contract. The importer does not load Orgo tables directly or write another component's store.

### Example 8 — Offline recovery

A sovereign node boots a verified recovery environment and imports a recovery bundle.

The same quarantine, parser, authority, replay, artifact, compatibility, and evidence controls apply. The recovered Release Set and component state become active only after recovery-specific validation and an atomic authority transition.
