<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-OPS-010",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "operations",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json#/data_authority_and_ownership",
    "contracts/system.contract.json#/cross_component_communication",
    "contracts/system.contract.json#/release_and_artifact_identity",
    "contracts/system.contract.json#/receipts_and_critical_transitions",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/integration-types.contract.json",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json",
    "contracts/components/identity-and-trust.component.json",
    "contracts/components/publication-gateway.component.json",
    "contracts/components/audit-broker.component.json",
    "contracts/artifact-contracts/sovereignty-bundle.schema.json",
    "contracts/artifact-contracts/offline-bundle.schema.json",
    "contracts/artifact-contracts/provenance-receipt.schema.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/exception-index.json"
  ],
  "decision_ids": [
    "DEC-DATA-001",
    "DEC-PROFILE-001",
    "DEC-GATE-001",
    "DEC-REL-001",
    "DEC-LIFE-001"
  ],
  "requirement_ids": [
    "REQ-OPS-EXIT-001",
    "REQ-OPS-EXIT-002",
    "REQ-OPS-EXIT-003",
    "REQ-OPS-EXIT-004",
    "REQ-OPS-EXIT-005",
    "REQ-OPS-EXIT-006",
    "REQ-OPS-EXIT-007",
    "REQ-OPS-EXIT-008",
    "REQ-OPS-EXIT-009",
    "REQ-OPS-EXIT-010",
    "REQ-OPS-EXIT-011",
    "REQ-OPS-EXIT-012",
    "REQ-OPS-EXIT-013",
    "REQ-OPS-EXIT-014",
    "REQ-OPS-EXIT-015",
    "REQ-OPS-EXIT-016",
    "REQ-OPS-EXIT-017",
    "REQ-OPS-EXIT-018",
    "REQ-OPS-EXIT-019",
    "REQ-OPS-EXIT-020",
    "REQ-OPS-EXIT-021",
    "REQ-OPS-EXIT-022",
    "REQ-OPS-EXIT-023",
    "REQ-OPS-EXIT-024",
    "REQ-OPS-EXIT-025",
    "REQ-OPS-EXIT-026",
    "REQ-OPS-EXIT-027",
    "REQ-OPS-EXIT-028",
    "REQ-OPS-EXIT-029",
    "REQ-OPS-EXIT-030"
  ],
  "lock_ids": [
    "LOCK-DOC-002",
    "LOCK-DOC-011",
    "LOCK-DOC-013",
    "LOCK-DOC-019",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-DATA-001",
    "LOCK-GATE-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-003",
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-007",
    "DOC-CONST-008",
    "DOC-CONST-009",
    "DOC-CONST-010",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-007",
    "DOC-SYS-008",
    "DOC-SYS-016",
    "DOC-SYS-019",
    "DOC-SYS-020",
    "DOC-LIFE-000",
    "DOC-SEC-002",
    "DOC-SEC-013",
    "DOC-SEC-015",
    "DOC-SEC-016",
    "DOC-OPS-000",
    "DOC-OPS-004",
    "DOC-OPS-006",
    "DOC-OPS-007"
  ],
  "tags": [
    "operations",
    "portability",
    "exit",
    "sovereignty-bundle",
    "export",
    "migration",
    "restore",
    "independent-recovery",
    "credentials",
    "integrations",
    "retention",
    "deletion",
    "receipts",
    "credible-exit"
  ]
}
KOA:DOC-META:END -->

# Portability and Exit

## 1. Purpose

This document defines the operational model for portability and credible exit.

Portability is the ability to move or reproduce in-scope data, artifacts, configuration, policies, identities, relationships, and evidence in a documented form.

Exit is the controlled transfer or closure of operational dependence on a deployment, provider, operator, environment, or integration.

The model distinguishes three outcomes:

```text
data portability
operational portability
complete exit
```

Data portability provides usable component-owned records and relationships.

Operational portability adds the artifacts, profiles, policies, trust context, configuration, dependencies, recovery material, and procedures needed to operate the exported state.

Complete exit adds cutover, revocation, integration closure, source retention or deletion, independent restoration, unresolved-obligation reporting, and final closure evidence.

A copied archive is not automatically portable. A successful restore attempt is not automatically an independent restoration. A destination service startup is not automatically a completed exit.

The architecture requires credible exit:

```text
exportable state
    → verified package
    → independent destination
    → controlled cutover
    → source closure
    → evidence of continuing autonomy
```

## 2. Scope

This document applies globally to portability and exit involving:

- tenant data;
- component-owned authoritative data;
- derived data and indexes;
- identity and trust context;
- governance policy;
- cultural-rights and consent records;
- UCKK objects and relationships;
- Ariane configuration and experience artifacts;
- Kristal, PGF, Atlas, language, and knowledge artifacts;
- system and service artifacts;
- active Release Sets;
- profiles and overlays;
- external integrations;
- external AI surfaces;
- SenTient where deployed;
- publication destinations;
- audit receipts and evidence;
- backups and recovery material;
- offline bundles;
- Sovereignty Bundles;
- source and destination credentials;
- retention, deletion, and legal or cultural holds.

It applies to:

- same-operator migration;
- operator change;
- provider change;
- node replacement;
- domain transfer;
- tenant export;
- sovereign-domain bootstrap;
- decommissioning;
- partial component exit;
- full deployment exit;
- recovery without the original operator.

This document does not define one mandatory archive format, database engine, cloud provider, storage appliance, transfer medium, orchestration platform, or legal exit period. Artifact contracts, profile contracts, component contracts, and active policy own those specifics.

## 3. Canonical References

The canonical sources for this document are:

```text
generated/authority-manifest.json
generated/decision-index.json
contracts/system.contract.json#/data_authority_and_ownership
contracts/system.contract.json#/cross_component_communication
contracts/system.contract.json#/release_and_artifact_identity
contracts/system.contract.json#/receipts_and_critical_transitions
generated/component-catalog.json
generated/profile-catalog.json
contracts/integration-types.contract.json
contracts/release-channels.contract.json
contracts/artifact-classes.contract.json
contracts/components/identity-and-trust.component.json
contracts/components/publication-gateway.component.json
contracts/components/audit-broker.component.json
contracts/artifact-contracts/sovereignty-bundle.schema.json
contracts/artifact-contracts/offline-bundle.schema.json
contracts/artifact-contracts/provenance-receipt.schema.json
generated/requirements-index.json
generated/assertion-index.json
generated/traceability.json
generated/test-catalog.json
generated/evidence-catalog.json
generated/exception-index.json
```

Their ownership roles are:

| Canonical source | Ownership |
| --- | --- |
| Component contracts | Authoritative export, import, data ownership, relationships, validation, and recovery |
| `data_authority_and_ownership` | Exclusive logical ownership and prohibited direct writes |
| `cross_component_communication` | Declared command, query, event, gateway, and artifact paths |
| Release and artifact registries | Artifact identity, four channels, Release Sets, compatibility, activation, and retention |
| Profile contracts | Required portability, offline, encryption, recovery, hardware, residency, and downtime behavior |
| Integration registry | External endpoint, credential, data, failure, removal, and closure behavior |
| Identity and Trust contract | Identity transfer, credential transition, trust roots, revocation, and destination trust |
| Publication Gateway contract | External publication state and destination closure |
| Audit Broker contract | Receipt preservation, verification, selective disclosure, and reconciliation |
| Sovereignty Bundle contract | Complete sovereign-domain portability container |
| Offline Bundle contract | Signed offline transport, sequence, trust, rollback, and application order |
| Provenance Receipt contract | Source, toolchain, environment, transformation, and publication lineage |
| `requirements.registry.json` | Normative portability and exit requirements |
| `locks.registry.json` | Profile, data, gateway, activation, recovery, and Release Set invariants |
| `traceability.registry.json` | Requirement, component, profile, artifact, test, and evidence relationships |
| `test-catalog.registry.json` | Export, import, restore, cutover, closure, and independent-recovery tests |
| `evidence.registry.json` | Portability, restoration, deletion, and closure evidence |
| `exceptions.registry.json` | Bounded deviations that cannot create opaque dependency or false closure |

This document explains operations. It does not become the canonical schema for exported component records or bundles.

## 4. Model and Responsibilities

### 4.1 Portability levels

| Level | Included scope |
| --- | --- |
| Data portability | Authoritative records, relationships, classifications, provenance, and owner schemas |
| Functional portability | Data plus compatible component artifacts and documented import behavior |
| Operational portability | Functional scope plus profiles, policies, trust, configuration, Release Set, backup, recovery, and operations |
| Complete exit | Operational scope plus cutover, revocation, source closure, integration closure, deletion or retention, and independent restoration |

The requested scope declares its level explicitly.

### 4.2 Exit object inventory

An exit inventory can include:

```text
tenant identities
component data exports
derived-data disclosures
artifact identities
Release Set
profiles and overlays
configuration
governance policy bundles
cultural-rights and consent policies
trust roots and revocation state
credential transition plan
integration manifests
external obligations
receipts and provenance
backups and checkpoints
recovery artifacts
retention and deletion schedule
reference and dependency graph
```

Each item has an owner and disposition.

### 4.3 Sovereignty Bundle

A Sovereignty Bundle is a lifecycle container for a bounded sovereign-domain transfer or bootstrap.

It can contain or reference:

- domain and tenant identity;
- target profiles;
- active Release Set;
- selected artifacts;
- component exports;
- trust and revocation material;
- policies;
- integration declarations;
- portability and recovery instructions;
- receipts and evidence;
- restoration order;
- rollback and forward-repair material.

It does not create a release channel.

An equivalent export can satisfy the same completeness when it is fully documented, verifiable, and independently restorable.

### 4.4 Component export contracts

Each component defines:

- exportable authoritative classes;
- excluded classes;
- derived-data handling;
- schema and version;
- stable identifiers;
- relationship encoding;
- classification and tenant scope;
- consent and rights metadata;
- integrity and provenance;
- import validation;
- conflict behavior;
- retention and deletion;
- recovery behavior.

The export coordinator invokes these contracts and does not bypass them with source-table access.

### 4.5 Reference preservation

References can connect:

- records within one component;
- records across components;
- artifacts;
- policies;
- identities;
- receipts;
- external destinations;
- published representations.

The package includes a reference map that distinguishes:

```text
resolved internally
resolved by another exported component
resolved by an included artifact
resolved by a destination-created identity
retained as historical reference
excluded with declared reason
unresolved and blocking
```

Silent reference loss is not acceptable.

### 4.6 Representation model

Portable representations use documented schemas and encodings.

A representation can be:

- canonical JSON;
- JSON Lines;
- CSV with a published schema;
- media files with manifests;
- signed artifact packages;
- database-neutral logical dumps;
- documented relational exports;
- content-addressed archives;
- a profile-approved standard interchange format.

An opaque physical backup can accompany the export but does not replace the logical representation required for independent restoration.

### 4.7 Identity and trust transition

Identity transition distinguishes:

| Identity class | Typical disposition |
| --- | --- |
| Tenant and subject identity | Transfer reference, map, or re-establish through approved identity proof |
| Service identity | Reissue under destination ownership |
| Node identity | Replace for destination nodes |
| Artifact signer trust | Preserve scoped trust and revocation evidence |
| Source operator credential | Revoke or retain only under declared residual obligation |
| External integration credential | Rotate, transfer through protected process, or revoke |
| Recovery credential | Reissue and verify under destination control |

Private keys are not included in ordinary data exports.

### 4.8 Release and artifact continuity

Portable deployments preserve artifact identity and channel membership.

The destination resolves:

```text
system selection
services selection
governance selection
knowledge selection
effective Release Set
profile and overlay compatibility
```

A destination can select a newer compatible Release Set through the ordinary lifecycle. It does not silently reinterpret exported artifacts.

### 4.9 External dependency closure

External dependencies include:

- integration credentials;
- API endpoints;
- callbacks and webhooks;
- queues;
- subscriptions;
- storage buckets;
- publication destinations;
- DNS names;
- certificates;
- provider-held data;
- external AI accounts;
- support access;
- monitoring and alert destinations;
- billing or contractual obligations.

Each dependency is transferred, replaced, revoked, closed, retained temporarily, or listed as unresolved.

### 4.10 Cutover phases

The operational phases are:

```text
planning
inventory
export preparation
source consistency boundary
export
package verification
transfer
destination quarantine
destination import
destination validation
cutover preparation
source write freeze
destination activation
observation
source deactivation
access revocation
retention and deletion
closure
```

The authoritative phase is machine-readable.

### 4.11 Write authority during cutover

The cutover contract identifies the single authoritative writer for every phase.

Supported strategies can include:

- planned source write freeze;
- bounded replication followed by final synchronization;
- event-log catch-up;
- owner-defined dual-read with one writer;
- component-specific migration transaction.

Uncontrolled active writes at both source and destination are prohibited.

### 4.12 Independent restoration

Independent restoration proves that an authorized destination operator can:

- obtain or possess the package;
- verify identities, digests, signatures, and provenance;
- provision compatible infrastructure;
- establish independent identity and trust;
- import component data;
- resolve relationships;
- activate compatible artifacts and policies;
- operate the system;
- back up and restore it;
- revoke access;
- export it again;
- recover without the original operator.

A test that relies on an undocumented original-provider control path does not prove independent restoration.

### 4.13 Retention and deletion

Source-side disposition categories include:

| Category | Disposition |
| --- | --- |
| Active source records | Freeze, transfer, retain temporarily, or delete under owner policy |
| Derived data | Rebuild, export, retain, restrict, or delete |
| Caches | Delete after validation unless needed for rollback |
| Backups | Retain or expire under recovery and hold policy |
| Receipts and provenance | Retain under evidence policy |
| Published copies | Track separately from local deletion |
| External provider copies | Request deletion or transfer and record verification state |
| Identifiers | Reserve permanently where required |

Exit closure records unresolved retained copies.

### 4.14 Credible exit evidence

A closure package can include:

- final inventory;
- export manifest;
- verification results;
- destination import and activation receipts;
- independent restoration result;
- cutover receipts;
- access-revocation evidence;
- integration closure status;
- source deactivation result;
- deletion and retention disposition;
- unresolved obligations;
- final owner acknowledgments;
- recourse path.

The evidence package uses selective disclosure.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-OPS-EXIT-001,REQ-OPS-EXIT-002,REQ-OPS-EXIT-003,REQ-OPS-EXIT-004,REQ-OPS-EXIT-005,REQ-OPS-EXIT-006,REQ-OPS-EXIT-007,REQ-OPS-EXIT-008,REQ-OPS-EXIT-009,REQ-OPS-EXIT-010,REQ-OPS-EXIT-011,REQ-OPS-EXIT-012,REQ-OPS-EXIT-013,REQ-OPS-EXIT-014,REQ-OPS-EXIT-015,REQ-OPS-EXIT-016,REQ-OPS-EXIT-017,REQ-OPS-EXIT-018,REQ-OPS-EXIT-019,REQ-OPS-EXIT-020,REQ-OPS-EXIT-021,REQ-OPS-EXIT-022,REQ-OPS-EXIT-023,REQ-OPS-EXIT-024,REQ-OPS-EXIT-025,REQ-OPS-EXIT-026,REQ-OPS-EXIT-027,REQ-OPS-EXIT-028,REQ-OPS-EXIT-029,REQ-OPS-EXIT-030 -->
- **REQ-OPS-EXIT-001 — SHALL:** Every portability or exit operation identify the requester, authority, tenant, source deployment, target or recipient, scope, purpose, included and excluded data classes, artifact classes, identities, trust material, policies, relationships, retention obligations, and expected closure condition.
- **REQ-OPS-EXIT-002 — SHALL:** Portability preserve canonical ownership, stable identifiers, tenant boundaries, data classifications, provenance, relationships, consent and cultural-rights context, retention, and evidence references.
- **REQ-OPS-EXIT-003 — SHALL:** A complete exit provide documented open or independently implementable representations for every in-scope authoritative data class and required relationship.
- **REQ-OPS-EXIT-004 — SHALL NOT:** A proprietary locator, mutable repository tag, undocumented database dump, opaque encrypted blob, or vendor-specific runtime state be the only available portability representation.
- **REQ-OPS-EXIT-005 — SHALL:** Each component export its own authoritative records through a declared export contract and preserve the distinction between authoritative, derived, cached, indexed, receipt, and artifact state.
- **REQ-OPS-EXIT-006 — SHALL NOT:** An exit coordinator read or write another component's authoritative source tables directly when an owner export or import contract exists.
- **REQ-OPS-EXIT-007 — SHALL:** A portability package include a machine-readable manifest, inventory, schema versions, content integrity evidence, provenance, dependency graph, reference map, compatibility declarations, and validation instructions.
- **REQ-OPS-EXIT-008 — SHALL:** A Sovereignty Bundle or equivalent complete export identify the active Release Set, selected artifacts, profiles, overlays, trust and revocation context, policy bundles, configuration, component data exports, receipts, recovery material, and restoration order.
- **REQ-OPS-EXIT-009 — SHALL NOT:** A Sovereignty Bundle, offline bundle, backup, export archive, or receipt create an additional release channel or replace the four-channel Release Set model.
- **REQ-OPS-EXIT-010 — SHALL:** Exported artifacts retain their canonical system, services, governance, or knowledge channel identity and exact artifact identity.
- **REQ-OPS-EXIT-011 — SHALL:** Secrets, credentials, private keys, recovery secrets, and integration tokens be excluded from ordinary exports or transferred only through an explicit protected credential-transition contract.
- **REQ-OPS-EXIT-012 — SHALL:** Identity, trust-root, credential, and revocation transitions define which identities transfer, which are reissued, which are revoked, which remain with the source operator, and how the destination establishes independent trust.
- **REQ-OPS-EXIT-013 — SHALL:** Exit plans close or transfer external integrations explicitly, including credentials, callbacks, endpoints, subscriptions, queues, pending transfers, provider-held data, deletion requests, and unresolved external obligations.
- **REQ-OPS-EXIT-014 — SHALL NOT:** Removal of an optional integration, external AI surface, SenTient workbench, publication destination, or original operator dependency break the native baseline or prevent independent restoration of in-scope data.
- **REQ-OPS-EXIT-015 — SHALL:** Portability exports apply minimization and selective disclosure so recipient authority does not receive unrelated tenants, secrets, restricted evidence, protected cultural content, or excluded data classes.
- **REQ-OPS-EXIT-016 — SHALL:** Consent, cultural-rights, audience, attribution, reuse, destination, residency, and retention constraints accompany every exported object or representation to which they apply.
- **REQ-OPS-EXIT-017 — SHALL:** A destination import remain quarantined until schema, identity, integrity, provenance, trust, profile, compatibility, malware or content checks where applicable, reference resolution, and owner acceptance complete.
- **REQ-OPS-EXIT-018 — SHALL:** Restoration validation prove that the destination can operate, query, update, back up, restore, revoke access, export again, and recover without the original operator's proprietary control path.
- **REQ-OPS-EXIT-019 — SHALL:** A complete exit include at least one verified independent restoration test or a profile-approved equivalent test against the exported package.
- **REQ-OPS-EXIT-020 — SHALL:** Migration and restoration preserve the active Release Set context or produce a new compatible Release Set before activation.
- **REQ-OPS-EXIT-021 — SHALL:** Cutover distinguish export completion, transfer completion, destination verification, destination activation, source write freeze, source deactivation, access revocation, retention closure, and final exit closure.
- **REQ-OPS-EXIT-022 — SHALL NOT:** Successful archive creation, transfer, destination receipt, restore attempt, or service startup be reported as completed exit without the required verification and closure states.
- **REQ-OPS-EXIT-023 — SHALL:** Cutover preserve rollback or forward-repair paths until destination operation, data integrity, identities, policies, integrations, backups, and recovery are validated.
- **REQ-OPS-EXIT-024 — SHALL:** Source-side deletion distinguish authoritative data, derived state, caches, backups, artifacts, receipts, legal or cultural holds, externally transferred copies, and permanently reserved identifiers.
- **REQ-OPS-EXIT-025 — SHALL NOT:** The source operator claim deletion from an external recipient or provider unless verified evidence confirms that outcome.
- **REQ-OPS-EXIT-026 — SHALL:** Every export, transfer, verification, import, activation, rollback, access revocation, integration closure, deletion, retention exception, and exit closure produce or reference machine-readable receipts when classified as critical.
- **REQ-OPS-EXIT-027 — SHALL:** Offline portability and exit use signed bundles, bounded parsing, quarantine, local trust and revocation state, sequence and rollback protection, durable local receipts, and later reconciliation where required.
- **REQ-OPS-EXIT-028 — SHALL:** An interrupted exit preserve an authoritative phase, prevent simultaneous uncontrolled writes at source and destination, and resume, roll back, or forward repair from recorded checkpoints.
- **REQ-OPS-EXIT-029 — SHALL:** Users, tenants, communities, operators, and authorized representatives receive truthful inventory, status, exclusions, unresolved obligations, deletion limits, verification results, challenge paths, and final closure evidence appropriate to their authority.
- **REQ-OPS-EXIT-030 — SHALL:** Profile-specific encryption, media, residency, bandwidth, downtime, database, container, orchestration, hardware, recovery, and retention controls remain explicit and cannot become global portability requirements through repetition.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Exit planning

Planning follows this sequence:

1. identify requester and authority;
2. define portability level and target;
3. identify tenants, components, profiles, and environments;
4. define timing, downtime, recovery, and closure requirements;
5. assign source and destination owners;
6. create the preliminary inventory;
7. identify external obligations;
8. define rollback and repair;
9. approve the plan;
10. record the plan receipt where required.

### 6.2 Inventory

Inventory:

1. queries every component owner;
2. enumerates authoritative and derived data;
3. enumerates artifacts and Release Set;
4. enumerates identities, trust, credentials, and policies;
5. enumerates integrations and destinations;
6. enumerates backups, receipts, and recovery material;
7. classifies each item as include, exclude, transform, regenerate, revoke, retain, or resolve;
8. records exclusions and blockers.

### 6.3 Export preparation

Preparation:

1. resolve export schemas and versions;
2. validate owner contracts;
3. establish the source consistency boundary;
4. create checkpoints where required;
5. prepare logical representations;
6. prepare artifact and policy manifests;
7. prepare identity and integration transition plans;
8. reserve bounded resources;
9. verify storage and transport capacity;
10. enter export-ready state.

### 6.4 Export

Export:

1. invokes each component's export interface;
2. preserves stable identifiers and tenant scope;
3. includes classifications, provenance, rights, and retention;
4. creates the reference map;
5. packages artifacts and policy context;
6. excludes ordinary secrets;
7. computes integrity evidence;
8. creates the manifest;
9. signs the lifecycle container where required;
10. records export completion.

### 6.5 Package verification

Verification:

1. validates manifest and schema;
2. verifies content digests and signatures;
3. resolves every required reference;
4. checks tenant and classification boundaries;
5. verifies artifact channels and Release Set;
6. verifies trust and revocation context;
7. checks portability completeness;
8. checks rollback and recovery material;
9. produces a verification receipt.

An incomplete package remains blocked.

### 6.6 Transfer and destination quarantine

Transfer:

1. validates recipient and destination;
2. applies encryption and media controls from the active profile;
3. transfers the immutable package;
4. verifies the received copy;
5. records transfer outcome;
6. places the package in destination quarantine;
7. avoids claiming import or activation.

### 6.7 Destination import

Import:

1. validates target profile and infrastructure;
2. validates schemas and artifact contracts;
3. establishes destination identities and trust;
4. imports component data through owner interfaces;
5. resolves references;
6. applies migrations;
7. stages artifacts and policies;
8. validates classifications, consent, rights, and retention;
9. leaves destination state non-authoritative until activation.

### 6.8 Destination validation

Validation:

1. tests component reads and writes;
2. tests cross-component contracts;
3. tests identity and policy;
4. tests artifact and Release Set compatibility;
5. tests external integration replacements;
6. tests backup and restore;
7. tests export from the destination;
8. tests recovery without the source operator;
9. records results.

### 6.9 Cutover

Cutover:

1. confirm destination readiness;
2. enter the source consistency boundary;
3. freeze or redirect writes under the approved strategy;
4. export final changes;
5. verify final synchronization;
6. activate destination artifacts, policies, and component state;
7. validate target health and authoritative identities;
8. mark destination authoritative;
9. deactivate source writes;
10. record cutover receipts.

### 6.10 Observation and rollback

During observation:

1. monitor component behavior and data integrity;
2. reconcile delayed events and integrations;
3. preserve rollback or repair material;
4. avoid source deletion;
5. roll back or forward repair when validation fails;
6. end observation only after acceptance criteria pass.

### 6.11 Access and integration closure

Closure:

1. revoke source operator and service access no longer required;
2. rotate destination credentials;
3. transfer or revoke integration credentials;
4. disable callbacks and subscriptions;
5. close publication destinations as required;
6. resolve provider-held data;
7. remove temporary transfer paths;
8. record unresolved obligations.

### 6.12 Source retention and deletion

Disposition:

1. classify every remaining source copy;
2. apply legal, cultural, recovery, and evidence holds;
3. delete or restrict eligible authoritative and derived data;
4. expire caches and temporary data;
5. retain receipts and identifiers;
6. request external deletion where applicable;
7. verify outcomes separately;
8. record the final source disposition.

### 6.13 Exit closure

Final closure:

1. confirm destination operation;
2. confirm independent restoration result;
3. confirm source deactivation;
4. confirm access revocation;
5. confirm integration disposition;
6. confirm retention and deletion;
7. list unresolved obligations;
8. provide the final inventory and evidence view;
9. record final owner acknowledgments;
10. create the exit-closure receipt.

### 6.14 Interrupted exit recovery

After interruption:

1. load the authoritative phase and checkpoints;
2. identify the active writer for every component;
3. compare source and destination state;
4. prevent new uncontrolled writes;
5. resume, roll back, or forward repair;
6. preserve receipts and evidence;
7. update status truthfully;
8. continue closure only after consistency is restored.

## 7. Failure States and Safe Degradation

| Failure code | Condition | Protected result | Safe degraded result |
| --- | --- | --- | --- |
| `exit_authority_missing` | Requester lacks authority for the export or exit | Operation is denied | Ordinary service continues |
| `exit_scope_incomplete` | Tenant, components, data, artifacts, identities, or closure scope is incomplete | Planning remains blocked | Complete the inventory |
| `exit_owner_export_missing` | A component lacks an active export contract | Complete exit is blocked | Partial export reports the exclusion |
| `exit_opaque_representation` | Export depends only on undocumented or proprietary state | Portability claim is denied | Produce a documented logical representation |
| `exit_reference_unresolved` | Required identifier or relationship cannot be resolved | Package verification fails | Repair the map or declare a blocking exclusion |
| `exit_schema_or_version_unsupported` | Destination cannot validate an export schema | Import remains blocked | Migrate through an approved version path |
| `exit_integrity_failed` | Package or contained object fails digest verification | Package is quarantined | Re-export or retransmit |
| `exit_signature_or_trust_failed` | Required signature or scoped trust fails | Import remains blocked | Resolve destination trust correctly |
| `exit_release_set_incompatible` | Exported artifacts and target profile are incompatible | Activation is denied | Select a compatible Release Set |
| `exit_secret_in_ordinary_export` | Export contains prohibited secret material | Package is rejected | Use protected credential transition |
| `exit_tenant_scope_violation` | Package includes an unauthorized tenant or object | Export is rejected | Regenerate a minimized package |
| `exit_rights_or_consent_context_missing` | Required rights metadata is absent | Affected object is excluded or quarantined | Restore the context |
| `exit_external_dependency_unresolved` | Integration, callback, provider data, or credential has no disposition | Exit closure is blocked | Transfer, revoke, retain, or disclose the obligation |
| `exit_destination_import_failed` | Component import cannot complete | Destination remains non-authoritative | Repair, retry, or roll back |
| `exit_destination_validation_failed` | Required operation, backup, restore, or export test fails | Cutover is denied | Repair destination |
| `exit_independent_restore_failed` | Destination depends on an undocumented source-operator path | Complete-exit claim is denied | Remove the dependency and retest |
| `exit_dual_writer_conflict` | Source and destination write simultaneously outside the approved strategy | Writes are frozen or isolated | Reconcile through the owner contract |
| `exit_cutover_partial` | Some components commit while required peers do not | Partial target remains non-authoritative | Rollback, repair, or enter recovery |
| `exit_access_revocation_incomplete` | Source or temporary access remains active | Exit remains closure-pending | Revoke and verify |
| `exit_external_deletion_unverified` | Provider-held deletion cannot be confirmed | Deletion is not reported complete | Record the unresolved external copy |
| `exit_retention_conflict` | Deletion conflicts with a hold, rollback, or evidence obligation | Deletion is blocked | Restrict use and retain |
| `exit_receipt_path_unavailable` | Critical phase lacks durable evidence | Cutover or closure is blocked | Preserve current authoritative state |
| `exit_status_ambiguous` | Authoritative phase or active writer cannot be determined | New writes and closure are blocked | Reconcile state |
| `exit_offline_sequence_invalid` | Offline bundle sequence or rollback protection fails | Import is denied | Use the last valid local state |

A failed destination import does not invalidate the source deployment. A failed deletion request does not undo a completed destination activation, but it blocks a false complete-deletion claim.

## 8. Cross-Component Interactions

### 8.1 Component owners

Each component owns its export, import, validation, correction, retention, deletion, and recovery behavior.

The exit coordinator orchestrates contracts without acquiring source-table authority.

### 8.2 Identity and Trust

Identity and Trust supports subject mapping, destination identities, scoped trust roots, credential transition, revocation, and signature verification.

The destination establishes independent trust rather than retaining hidden control by the source operator.

### 8.3 Lifecycle services

Lifecycle services verify, stage, activate, roll back, repair, and retain artifacts under the effective Release Set.

They distinguish data import from artifact activation.

### 8.4 Publication Gateway

Publication Gateway tracks published representations and external destinations.

Exit closure identifies which publications remain externally available, transferred, withdrawn, or unresolved.

### 8.5 Audit Broker

Audit Broker preserves receipts and creates authorized evidence views.

It does not receive unrestricted component exports merely because it stores exit receipts.

### 8.6 Resource Governor

Resource Governor bounds export, verification, transfer, import, migration, backup, restore, and deletion workloads.

Capacity does not authorize the exit.

### 8.7 External integrations

Integration owners define transfer, rotation, revocation, callback, provider-data, and removal behavior.

Optional integrations can be removed without blocking independent native operation.

### 8.8 Backup and recovery

Backup and recovery services provide verified checkpoints and destination restore tests.

A physical backup complements but does not replace the component-level portable export.

### 8.9 Profiles and overlays

Profiles define encryption, media, bandwidth, downtime, hardware, residency, offline, and recovery controls.

High-assurance or sovereign profiles can require stronger evidence and isolation without changing global ownership.

### 8.10 Users, tenants, and communities

Authorized parties receive an appropriate inventory, exclusions, rights constraints, status, unresolved obligations, deletion limitations, and recourse information.

The view remains selectively disclosed.

## 9. Decision Closure and Prohibited Assumptions

This document closes the portability and exit interpretation as follows:

- portability has data, functional, operational, and complete-exit levels;
- components own their exports and imports;
- documented logical representations are required for independent restoration;
- Sovereignty Bundles are lifecycle containers, not release channels;
- the four-channel Release Set remains explicit;
- identity and trust transition is separate from ordinary data export;
- secrets use protected transition paths;
- external dependencies require explicit disposition;
- optional integrations cannot become hidden exit blockers;
- destination import remains quarantined until accepted;
- independent restoration is tested;
- cutover has one authoritative writer per phase;
- source deletion occurs after destination validation and observation;
- external deletion is reported only when verified;
- receipts distinguish every critical phase;
- interrupted exits resume from authoritative checkpoints;
- final closure reports unresolved obligations truthfully.

The following assumptions are prohibited:

- a database dump alone proves portability;
- a backup controlled by the original operator proves independent restoration;
- a proprietary container image is a complete export;
- an offline bundle creates a fifth release channel;
- copied private keys are the default identity-transfer method;
- destination startup proves successful import;
- transfer completion proves exit closure;
- destination activation permits immediate source deletion automatically;
- a shared provider account can remain indefinitely without disclosure;
- external AI or publication-provider data is deleted because the local copy was deleted;
- derived data can be omitted without disposition;
- identifiers can be reused after exit;
- a destination can ignore consent or cultural-rights metadata;
- dual writers are acceptable during an unbounded transition;
- profile-specific media or encryption rules apply globally.

A new global portability level, implicit identity-transfer mechanism, opaque mandatory representation, release-channel change, or false-closure semantic requires an accepted owner decision and complete impact validation.

## 10. Validation Criteria

This document is conformant when all of the following checks pass:

1. the metadata block is first, valid, and declares status `active`;
2. the document contains the required 11 normative sections;
3. all 30 requirement identifiers are unique and registered;
4. every declared decision is accepted;
5. every declared lock exists and is active;
6. every requested exit declares level, source, target, scope, authority, owners, downtime, recovery, and closure;
7. every component has a validated export and import contract for in-scope authoritative data;
8. exported representations are documented and independently implementable;
9. inventory tests cover data, artifacts, Release Set, policies, identities, integrations, receipts, backups, and recovery;
10. reference tests resolve or explicitly block every required relationship;
11. package tests validate manifest, schemas, digests, signatures, provenance, compatibility, and instructions;
12. release tests preserve exactly the system, services, governance, and knowledge channel model;
13. secret tests reject ordinary export of credentials, private keys, and recovery secrets;
14. identity tests cover mapping, reissue, revocation, destination trust, and source-operator removal;
15. privacy tests preserve tenant, classification, consent, rights, audience, retention, and selective disclosure;
16. integration tests cover endpoints, callbacks, credentials, pending operations, provider data, deletion, and removal;
17. destination tests cover quarantine, owner imports, reference resolution, migrations, and activation;
18. independent-restoration tests operate without proprietary source-operator control paths;
19. destination tests cover reads, writes, backups, restores, revocation, re-export, and recovery;
20. cutover tests prove one authoritative writer per phase;
21. rollback and forward-repair tests preserve data ownership and Release Set compatibility;
22. source-access tests revoke obsolete human, service, integration, and temporary access;
23. deletion tests distinguish authoritative, derived, cache, backup, receipt, published, and external copies;
24. external deletion tests distinguish request from verified outcome;
25. receipt tests cover export, transfer, verification, import, activation, rollback, revocation, integration closure, deletion, retention exceptions, and closure;
26. offline tests cover signed bundles, parsing limits, quarantine, sequence, rollback protection, local receipts, and reconciliation;
27. interruption tests recover the authoritative phase and active-writer state;
28. user and tenant evidence views report scope, exclusions, results, unresolved obligations, and recourse;
29. profile tests keep encryption, media, residency, bandwidth, downtime, database, container, orchestration, hardware, recovery, and retention controls profile-scoped;
30. no unresolved-authority marker, duplicate identifier, or unregistered normative statement exists;
31. active prose is English;
32. ordinary Markdown validation does not depend on file-content hashes.

Expected validator failure codes include:

```text
exit_authority_missing
exit_scope_incomplete
exit_owner_export_missing
exit_opaque_representation
exit_reference_unresolved
exit_schema_or_version_unsupported
exit_integrity_failed
exit_signature_or_trust_failed
exit_release_set_incompatible
exit_secret_in_ordinary_export
exit_tenant_scope_violation
exit_rights_or_consent_context_missing
exit_external_dependency_unresolved
exit_destination_import_failed
exit_destination_validation_failed
exit_independent_restore_failed
exit_dual_writer_conflict
exit_cutover_partial
exit_access_revocation_incomplete
exit_external_deletion_unverified
exit_retention_conflict
exit_receipt_path_unavailable
exit_status_ambiguous
exit_offline_sequence_invalid
```

## 11. Non-Normative Examples

### 11.1 Tenant data portability

A tenant requests a data-portability export. Each component provides its authoritative records and relationship map. The package includes classifications, consent and rights context, provenance, and documented schemas, but excludes other tenants and operator credentials.

### 11.2 Sovereign operator change

A sovereign domain moves to a new operator. A Sovereignty Bundle contains the active Release Set, component exports, profiles, policies, trust and revocation context, integrations, receipts, and recovery material. Destination service and node identities are reissued under the new operator.

### 11.3 Independent restoration

A destination team restores the package in a clean environment using only the documented schemas, artifacts, profiles, trust bootstrap, and recovery instructions. It verifies backup, restore, revocation, re-export, and recovery without the source operator.

### 11.4 External AI closure

An optional external AI integration is removed during exit. Credentials are revoked, callbacks are closed, provider-held data receives a deletion request, and the unresolved verification state is reported. Native local capabilities continue.

### 11.5 Interrupted cutover

A cutover stops after two components import but before destination activation. The recorded phase shows the source remains authoritative. Destination state remains quarantined, final changes are reconciled, and cutover resumes without uncontrolled dual writes.
