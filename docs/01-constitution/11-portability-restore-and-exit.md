<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-CONST-011",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "constitution",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json#/portability",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/artifact-classes.contract.json",
    "contracts/release-channels.contract.json",
    "contracts/integration-types.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-PORT-001",
    "DEC-LIFE-001",
    "DEC-RECEIPT-001",
    "DEC-SEC-001",
    "DEC-DATA-001",
    "DEC-COMP-001",
    "DEC-INTEGRATION-001",
    "DEC-OFFLINE-001",
    "DEC-AUDIT-001",
    "DEC-PRIV-001",
    "DEC-KRISTAL-001",
    "DEC-LANG-001"
  ],
  "requirement_ids": [
    "REQ-CONST-PORT-001",
    "REQ-CONST-PORT-002",
    "REQ-CONST-PORT-003",
    "REQ-CONST-PORT-004",
    "REQ-CONST-PORT-005",
    "REQ-CONST-PORT-006",
    "REQ-CONST-PORT-007",
    "REQ-CONST-PORT-008",
    "REQ-CONST-PORT-009",
    "REQ-CONST-PORT-010",
    "REQ-CONST-PORT-011",
    "REQ-CONST-PORT-012",
    "REQ-CONST-PORT-013",
    "REQ-CONST-PORT-014",
    "REQ-CONST-PORT-015",
    "REQ-CONST-PORT-016"
  ],
  "lock_ids": [
    "LOCK-DATA-001",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-GATE-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-AI-001",
    "LOCK-AI-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-000",
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-007",
    "DOC-CONST-008",
    "DOC-CONST-009",
    "DOC-CONST-010",
    "DOC-GOV-001",
    "DOC-GOV-002",
    "DOC-GOV-009",
    "DOC-GOV-010",
    "DOC-GOV-015"
  ],
  "tags": [
    "constitution",
    "portability",
    "export",
    "backup",
    "restore",
    "recovery",
    "credible-exit",
    "data-ownership",
    "trust-handover",
    "independent-consumption",
    "evidence"
  ]
}
KOA:DOC-META:END -->

# Portability, Restore, and Credible Exit

## 1. Purpose

This document defines the constitutional rules that prevent authoritative user and organizational data from becoming trapped by an operator, deployment, component implementation, integration, storage engine, or unavailable service.

It establishes the common meaning of:

- portable authoritative data;
- complete and controlled export;
- backup and recovery material;
- verified restore;
- independent consumption;
- protected trust handover;
- credible exit;
- portability evidence.

The constitutional objective is not merely to copy bytes. It is to preserve enough declared structure, authority, policy, trust, identity, and operational meaning for authorized data to remain usable after transfer.

Detailed operational schedules, storage locations, backup procedures, restore runbooks, disaster recovery, and profile-specific recovery objectives are owned by lifecycle and operations documentation. This document constrains those details without replacing them.

Canonical facts remain owned by the referenced registries. This document explains their constitutional effect and presents the applicable requirements generated from `generated/requirements-index.json`.

## 2. Scope

This document applies globally to:

- authoritative user and organizational data;
- component-owned operational state;
- identity and delegation records required for lawful continuity;
- governance policy and consent state;
- Kristal artifacts and references;
- language and runtime artifacts required to interpret authoritative content;
- declared audit and evidence classes;
- release and artifact identities required for compatibility;
- recovery metadata;
- integration configuration needed to understand, disable, or replace an optional dependency;
- profile-specific backup, restore, and exit envelopes.

It governs:

- full and scoped exports;
- backup packages used as restore inputs;
- component-to-component export coordination;
- restoration into a compatible environment;
- re-import into a replacement deployment;
- independent consumption by documented tools;
- operator handover;
- migration between supported deployments;
- exit testing and conformance claims.

It does not grant access to data, secrets, keys, or evidence. Every export, restore, and handover remains subject to applicable identity, authority, consent, disclosure, retention, security, and profile rules.

A cache, replica, storage snapshot, database dump, container volume, object-store copy, or filesystem archive is not automatically a constitutional portability package.

## 3. Canonical References

| Canonical reference | Responsibility in this document |
| --- | --- |
| `generated/authority-manifest.json` | Active authority release, ownership map, validation policy, and cutover state |
| `generated/decision-index.json` | Accepted portability, lifecycle, security, data, integration, and evidence decisions |
| `contracts/system.contract.json#/portability` | Global portability, restore, independent-consumption, and exit model |
| `generated/component-catalog.json` | Component responsibilities and authoritative data ownership |
| `generated/profile-catalog.json` | Profile-specific portability, restore, recovery, and external-dependency envelopes |
| `contracts/artifact-classes.contract.json` | Artifact identity, inclusion, activation, compatibility, and retention rules |
| `contracts/release-channels.contract.json` | Release identities and compatibility boundaries |
| `contracts/integration-types.contract.json` | Integration classification, removability, exported configuration, and data-transfer constraints |
| `generated/requirements-index.json` | Normative portability requirements and validation mappings |
| `generated/assertion-index.json` | Cross-file ownership, lifecycle, profile, gateway, and AI alignment assertions |
| `generated/traceability.json` | Decision, requirement, test, evidence, profile, component, and document relationships |
| `generated/exception-index.json` | Explicit and bounded deviations with compensating controls |
| `generated/test-catalog.json` | Export, restore, re-import, independent-consumption, and exit tests |
| `generated/evidence-catalog.json` | Test evidence, receipts, validity, retention, and disclosure classes |

The following documents provide detailed implementation and operational interpretation without becoming alternate canonical owners:

```text
06-lifecycle/14-recovery.md
08-operations/08-backup.md
08-operations/09-restore.md
08-operations/10-portability-and-exit.md
08-operations/13-disaster-recovery.md
09-conformance/
11-recipes/sovereign-linux/backup-and-restore.md
```

Repository-relative paths and canonical object identifiers are the only authority references used by this document.

## 4. Model and Responsibilities

### 4.1 Portability

Portability is the ability to extract authorized authoritative state in documented forms while preserving the identifiers, relationships, ownership boundaries, policy context, artifact references, and compatibility information needed for continued lawful use.

Portability can be demonstrated through:

- successful re-import into a compatible kOA deployment;
- successful restoration onto a clean compatible environment;
- successful independent consumption by a documented non-kOA implementation;
- a combination of these paths where one path cannot represent every governed capability.

Portability does not require every internal implementation detail to remain identical. It requires preserved meaning, declared transformations, and verifiable continuity of authoritative state.

### 4.2 Backup

A backup is protected recovery material captured for restoration after loss, corruption, operational failure, or disaster.

A backup may contain implementation-specific representation. It remains subject to:

- encryption;
- integrity protection;
- authorization;
- retention;
- isolation from active state;
- restore testing;
- profile-specific recovery objectives.

A backup may contribute to portability, but its existence alone does not demonstrate portability or restore success.

### 4.3 Export

An export is an authorized extraction produced through declared component or system contracts.

An export identifies:

- its subject and scope;
- the owning components;
- included and excluded data classes;
- source and target schema versions;
- artifact and release dependencies;
- policy, consent, and disclosure constraints;
- trust dependencies;
- ordering and reconstruction rules;
- validation and import instructions.

An ordinary export excludes private signing keys, privileged credentials, and unrestricted secret material.

### 4.4 Restore

A restore reconstructs authoritative state from an approved backup or portability package in a declared compatible environment.

A restore has three phases:

1. **Preflight:** validate identity, authorization, package completeness, compatibility, trust, policy, consent, artifacts, and required migrations.
2. **Staged reconstruction:** restore component-owned state without exposing a partially authoritative system.
3. **Activation and verification:** activate the restored version set, verify health and invariants, and emit evidence.

A failed or incomplete restore remains non-authoritative and cannot be represented as successful.

### 4.5 Credible exit

Credible exit is the demonstrated ability of an authorized subject to leave the original operator, deployment, or integration without losing lawful access to its authoritative data or becoming dependent on undocumented private state.

Credible exit requires more than documentation. It requires an executed and evidenced transfer path.

The path proves that:

- the original operator is not required for ordinary continued use;
- required data can be restored or independently consumed;
- trust and identity continuity is handled explicitly;
- optional integrations can be removed or replaced;
- critical workflows can resume;
- restrictions and consent remain enforceable;
- known losses or unsupported capabilities are declared.

### 4.6 Responsibility allocation

| Responsibility | Owner |
| --- | --- |
| Global portability model | `contracts/system.contract.json#/portability` |
| Authoritative data boundaries | `generated/component-catalog.json` and component contracts |
| Profile recovery and exit envelope | Applicable profile contract |
| Export format and component mapping | Owning component contract or artifact contract |
| Release and artifact compatibility | Release-channel and artifact-class registries |
| Authorization, consent, and disclosure decisions | Owning component and Governance Policy Runtime where deployed |
| Trust and protected credential handover | Identity and Trust component and applicable security contract |
| Selective evidence export | Audit Broker and evidence registry |
| Resource scheduling for export and restore jobs | Resource Governor |
| Restore orchestration | Applicable lifecycle and operations contracts |
| Exit conformance | Test catalog, evidence registry, and conformance documentation |

No centralized export process becomes the owner of component data merely because it coordinates a package.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-CONST-PORT-001,REQ-CONST-PORT-002,REQ-CONST-PORT-003,REQ-CONST-PORT-004,REQ-CONST-PORT-005,REQ-CONST-PORT-006,REQ-CONST-PORT-007,REQ-CONST-PORT-008,REQ-CONST-PORT-009,REQ-CONST-PORT-010,REQ-CONST-PORT-011,REQ-CONST-PORT-012,REQ-CONST-PORT-013,REQ-CONST-PORT-014,REQ-CONST-PORT-015,REQ-CONST-PORT-016 -->
- **REQ-CONST-PORT-001 — SHALL:** Every component that owns authoritative user or organizational data provides a documented export path for that owned state.
- **REQ-CONST-PORT-002 — SHALL:** A complete portability export identifies its scope, subject, component sources, schema versions, artifact versions, policy versions, trust dependencies, creation time, and required restore sequence.
- **REQ-CONST-PORT-003 — SHALL:** Export formats are documented, machine-readable where applicable, and usable without an undocumented dependency on the original operator.
- **REQ-CONST-PORT-004 — SHALL:** A portability export preserves the relationships required to reconstruct valid authoritative state, including stable identifiers, ownership boundaries, references, and declared ordering constraints.
- **REQ-CONST-PORT-005 — SHALL:** A restore validates package identity, authorized scope, compatibility, schemas, migrations, trust dependencies, artifacts, policy state, consent state, and post-restore health before restored state becomes authoritative.
- **REQ-CONST-PORT-006 — SHALL NOT:** A backup, snapshot, replica, export, or copied storage directory be treated as proof of successful restore.
- **REQ-CONST-PORT-007 — SHALL:** A credible exit claim includes a successful restore, re-import, or independent-consumption test performed in an environment that does not depend on the original operator's private runtime state.
- **REQ-CONST-PORT-008 — SHALL:** The exit test proves that authorized workflows, ownership boundaries, policy evaluation, required indexes, artifact references, and critical evidence remain usable after transfer.
- **REQ-CONST-PORT-009 — SHALL:** Each deployment profile declares the data classes, artifact classes, trust material, recovery objectives, and external dependencies included in its portability and restore envelope.
- **REQ-CONST-PORT-010 — SHALL:** Secrets, private signing keys, recovery keys, and privileged credentials are excluded from ordinary exports and transferred only through an explicitly authorized protected handover procedure.
- **REQ-CONST-PORT-011 — SHALL:** Rights, consent, disclosure, retention, deletion, and cultural-governance constraints remain attached to exported and restored data.
- **REQ-CONST-PORT-012 — SHALL:** Audit and evidence exports disclose only authorized classes and preserve the information required to verify critical transitions without becoming unrestricted data dumps.
- **REQ-CONST-PORT-013 — SHALL:** Optional integrations remain removable, and their removal does not prevent export, restore, or independent consumption of core authoritative state.
- **REQ-CONST-PORT-014 — SHALL:** Unavailable immutable artifacts are included in the portability package unless their independent availability, identity, compatibility, and retrieval path are verified.
- **REQ-CONST-PORT-015 — SHALL:** Every export, restore, and credible-exit test produces machine-readable evidence containing the applicable versions, scope, executor, result, failures, and exceptions.
- **REQ-CONST-PORT-016 — SHALL NOT:** A partial, failed, blocked, unverified, or exception-dependent transfer be represented as a complete portability, restoration, or credible-exit success.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Export and Handover Procedure

### 6.1 Initiation

The requesting actor identifies:

- the authorized subject;
- the export purpose;
- the requested scope;
- the target environment or independent consumer;
- the expected handover method;
- applicable retention and deletion obligations;
- whether trust material requires protected transfer.

The authority path resolves the applicable policy, consent, disclosure, profile, component, integration, and evidence rules before extraction begins.

### 6.2 Component-owned extraction

Each owning component produces or authorizes the export of its own authoritative state.

The extraction process:

1. freezes or records a consistent logical point;
2. records the source version set;
3. exports stable identifiers and declared relationships;
4. preserves ownership and scope information;
5. includes required schema and migration information;
6. excludes undeclared implementation caches;
7. applies disclosure, retention, redaction, and consent controls;
8. emits a component-level export result.

A coordinating process may assemble these outputs but does not bypass component contracts.

### 6.3 Package composition

A complete package includes, when applicable:

```text
package manifest
subject and scope declaration
component export inventory
schema and format descriptions
release and artifact identities
governance policy references or portable policy state
rights and consent records
identity and delegation records permitted for transfer
Kristal artifacts or independently retrievable references
language and runtime artifacts required for interpretation
authorized audit and evidence classes
integration dependency declarations
restore and independent-consumption instructions
validation and compatibility rules
test definitions and expected results
```

Immutable artifacts may be referenced rather than embedded only when their independent retrieval, identity, compatibility, and continued availability have been verified.

### 6.4 Trust material

Ordinary export packages do not contain raw private signing keys, privileged credentials, recovery secrets, or unrestricted root-of-trust material.

Trust continuity uses one of the following declared paths:

- new keys and identities are enrolled at the destination;
- public trust material and delegation records are transferred;
- a protected handover profile transfers approved private material under stronger authorization, encryption, dual control, and evidence;
- historical signatures remain verifiable while future authority begins under newly enrolled keys.

Recovery of a key does not automatically authorize its continued use.

### 6.5 Package validation

Before release to the authorized recipient, the package is checked for:

- complete inventory;
- resolvable component ownership;
- valid scope;
- schema and artifact consistency;
- absence of undeclared secrets;
- retention and consent compliance;
- selective audit disclosure;
- declared external dependencies;
- import or independent-consumption readiness;
- required evidence.

A partial package can be issued only when its limitations are explicit and it is not represented as a complete exit package.

## 7. Restore, Re-import, and Independent Exit

### 7.1 Clean compatible environment

A credible restore or exit test uses an environment that:

- is clean or demonstrably isolated from the source deployment;
- satisfies the target profile's compatibility requirements;
- has declared release, artifact, storage, trust, and resource prerequisites;
- can operate without undocumented source-operator services;
- can access only the declared external dependencies.

The environment may be a replacement kOA node or a documented independent consumer, depending on the capability being tested.

### 7.2 Preflight validation

Before state reconstruction, the restore process verifies:

1. package identity and completeness;
2. actor and recipient authorization;
3. subject and scope;
4. schema and migration compatibility;
5. release and artifact compatibility;
6. encryption and key availability;
7. identity, trust, and delegation continuity;
8. governance policy and consent state;
9. retention, withdrawal, and deletion constraints;
10. component ownership and reconstruction order;
11. required capacity and offline dependencies;
12. applicable exceptions.

A failed preflight blocks activation.

### 7.3 Staged reconstruction

Component state is restored through each component's declared import or recovery contract.

The process does not perform direct cross-component table writes.

Derived indexes, previews, caches, search structures, and read models are rebuilt from canonical restored state unless their artifact contract explicitly permits verified restoration.

The restored state remains staged until all required component, system, profile, security, and lifecycle checks pass.

### 7.4 Activation

Activation occurs only after the complete compatible version set is available.

The activation process:

- establishes the destination authority set;
- confirms the intended owning components;
- activates required policy and trust state;
- verifies critical workflows;
- verifies local and offline behavior;
- confirms that optional integrations can be disabled;
- records the final result.

Partial activation is treated as failure unless an explicit recovery state defines safe read-only access.

### 7.5 Exit proof

A credible exit test demonstrates all applicable outcomes:

- the package can be imported or independently consumed;
- authoritative records remain identifiable and correctly owned;
- references and ordering constraints remain valid;
- critical workflows resume;
- policy and consent remain enforceable;
- required artifacts remain available;
- audit and evidence remain selectively verifiable;
- the original operator is not required for ordinary continued use;
- known unsupported features or losses are declared;
- the result is recorded in the evidence registry.

A test executed only against the original active environment does not prove independent exit.

## 8. Failure States and Safe Degradation

| Failure condition | Required behavior | Permitted state | Prohibited claim | Required evidence |
| --- | --- | --- | --- | --- |
| Package inventory is incomplete | Stop preflight or issue a declared partial export | Source system remains authoritative | Complete export or credible exit | Missing-item report |
| Package identity or integrity cannot be verified | Reject the package | Previously valid state only | Restore success | Integrity failure result |
| Recipient authority or consent is absent | Deny export or restore | Existing authorized local use | Transfer authorization | Policy rejection |
| Required schema or migration path is unavailable | Block activation | Staged package inspection when permitted | Compatible restore | Compatibility result |
| Required key is unavailable | Keep protected state inaccessible | Restore of independent unprotected classes when explicitly permitted | Complete restore | Key-dependency result |
| Trust handover is invalid | Reject future authority activation | Historical signature verification where possible | Trust continuity | Trust validation result |
| Immutable artifact reference cannot be independently retrieved | Treat package as incomplete unless the artifact is embedded | Unaffected data inspection | Complete portability | Artifact availability result |
| Optional integration is unavailable | Disable integration-dependent features | Core exported and restored state | Full integration continuity | Integration degradation record |
| Derived index rebuild fails | Keep affected capability unavailable or read-only | Canonical restored data when safe | Full operational recovery | Rebuild failure result |
| Cross-component ownership cannot be reconstructed | Block activation | Staged inspection | Authoritative restore | Ownership conflict result |
| Restricted evidence would be over-disclosed | Redact, separate, or deny the evidence export | Authorized evidence classes | Complete unrestricted audit export | Disclosure decision |
| Exit test still depends on original private services | Mark the test failed | Source deployment remains usable | Credible independent exit | Dependency analysis |
| Required test evidence is absent | Mark the claim unproven | Previously established claims only | New restore or exit success | Missing-evidence result |
| Exception changes the expected capability | Report the bounded exception and limitation | Scope explicitly allowed by the exception | Unqualified success | Exception and compensating-control evidence |

Safe degradation preserves valid source state and explicitly safe read-only capabilities. It does not convert an incomplete transfer into a successful exit, weaken consent, bypass ownership, or invent a replacement trust path.

## 9. Cross-Component Interactions

### 9.1 Export coordinator and owning components

An export coordinator requests scoped exports from owning components.

Each component:

1. validates authority for its own data;
2. applies retention, consent, and disclosure rules;
3. produces a documented component export;
4. records included and excluded classes;
5. returns an export result.

The coordinator assembles the package and manifest. It does not read or mutate private component storage outside declared interfaces.

### 9.2 Identity and Trust

Identity and Trust provides the authorized identity, delegation, public trust material, protected handover path, and destination enrollment process.

It does not place raw private keys into ordinary exports.

### 9.3 Governance Policy Runtime

Where deployed, Governance Policy Runtime evaluates export, disclosure, consent, retention, emergency, and handover policy.

It returns policy decisions and does not perform data extraction or restoration itself.

### 9.4 Audit Broker and evidence registry

Audit Broker exports only authorized evidence classes with declared scope, time range, redaction, recipient authority, and retention.

The evidence registry records test and transition evidence. Neither becomes an unrestricted copy of all operational data.

### 9.5 Kristal and language artifacts

Kristal identity remains derived from canonical epistemic content rather than workflow state, interface metadata, or storage paths.

Language artifacts required to interpret exported content are included or independently retrievable under declared identities and compatibility rules.

### 9.6 UCKK and publication boundaries

UCKK exports preserve source media identity, metadata, ownership, restrictions, deterministic derivatives, and artifact relationships.

Restricted content remains restricted in originals, previews, indexes, manifests, and exports.

Publication Gateway controls governed disclosure. A portability export does not automatically publish its content.

### 9.7 Resource Governor

Resource Governor schedules export, validation, rebuild, and restore jobs according to the active profile.

It does not authorize the transfer and cannot change the declared completeness of a failed or partial package.

### 9.8 External integrations

Integration adapters disclose their exported configuration, transferred data classes, replacement requirements, and removal behavior.

No optional integration becomes an undocumented mandatory intermediary for export, restore, or independent consumption.

## 10. Decision Closure and Validation

This document is supported by the accepted decisions declared in its metadata.

A semantic change requires:

1. an accepted owner decision;
2. identification of affected system, profile, component, artifact, integration, security, lifecycle, operations, conformance, and migration objects;
3. direct and transitive impact analysis;
4. updates to requirements, locks, tests, evidence, and dependent documents;
5. complete validation before authority activation.

The following assumptions are prohibited:

- a backup proves restore because it completed without error;
- a storage snapshot is a portable export;
- an export is complete because every database file was copied;
- undocumented binary formats are portable because the original software can still read them;
- a cloud or external integration may remain a hidden restore dependency;
- direct database writes are acceptable during restoration;
- rebuilding caches can replace missing authoritative data;
- transferred consent for one purpose authorizes a different purpose;
- raw private keys belong in ordinary exit packages;
- historical audit data may be disclosed without class and recipient authorization;
- a restore on the original active node proves independent exit;
- the original operator's credentials, private services, or undocumented knowledge may remain necessary;
- a partial package can be labeled complete;
- an exception-dependent success can be reported without its limitation;
- documentation alone proves that a restore or exit path works.

This document is conformant when:

1. it is registered as `DOC-CONST-011`, classed as `normative_markdown`, and active in global scope;
2. every canonical reference resolves to an active object;
3. `DEC-PORT-001` and all supporting decisions are accepted;
4. every declared requirement is unique, active, globally scoped, and testable;
5. all declared locks exist and applicable assertions pass;
6. each authoritative data owner has a documented export and restore mapping;
7. profile contracts declare their portability and recovery envelopes;
8. ordinary exports exclude secrets and private signing keys;
9. export packages preserve policy, consent, ownership, identity, and compatibility information;
10. restore tests use clean compatible environments and declared dependencies;
11. exit tests prove re-import, restoration, or independent consumption without the original operator;
12. optional integrations can be removed without loss of core authoritative data;
13. failed, partial, blocked, and exception-limited results are represented accurately;
14. required tests and evidence resolve through traceability;
15. no parallel authority or unresolved migration source governs the active model;
16. the active text is English and contains the complete required section structure.

Applicable failure codes include:

```text
portability_owner_missing
export_scope_invalid
export_inventory_incomplete
export_secret_exposure
export_policy_context_missing
artifact_dependency_unavailable
restore_compatibility_failed
restore_trust_failed
restore_partial_activation
independent_exit_dependency_detected
consent_continuity_failed
cross_component_restore_write
portability_evidence_missing
credible_exit_unproven
```

A required validator that cannot run produces `blocked`, not `pass`.

## 11. Non-Normative Examples

### Example 1 — Component export

An organization requests a complete authorized export.

Konnaxion, Orgo, UCKK, Identity and Trust, Governance Policy Runtime, Kristal, and Audit Broker each produce scoped outputs through their own contracts. A coordinator assembles the manifest and records exclusions. The coordinator never becomes the owner of those domains.

### Example 2 — Backup without restore evidence

A nightly encrypted backup completes successfully.

The deployment may record backup completion, but it cannot claim proven restoration. A scheduled test must restore the selected data classes into a clean compatible environment and verify health.

### Example 3 — Independent consumer

An authorized subject exports records in documented open forms and verifies that an independent tool can parse, relate, and preserve the data.

Capabilities requiring a kOA-specific runtime may be represented by documented artifacts and references. The test records which functions remain available and which do not.

### Example 4 — Protected trust handover

A sovereign deployment transfers authority to a new operator.

Public trust material and delegation history are exported normally. Future signing authority begins with newly enrolled destination keys. A private key is transferred only when a protected handover profile explicitly authorizes it.

### Example 5 — Removed integration

A deployment previously used an optional remote synchronization service.

The service is disabled before the exit test. The package still exports and restores core authoritative state. Synchronization history and remote-only capabilities are documented, but the missing service does not prevent local continued use.

### Example 6 — Partial historical evidence

An authorized audit export excludes evidence classes that the recipient is not permitted to receive.

The package remains a valid scoped evidence export. It is not labeled a complete unrestricted audit archive, and its manifest records the authorized exclusions.
