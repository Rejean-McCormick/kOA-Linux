<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-ADR-025",
  "document_class": "adr",
  "status": "accepted",
  "language": "en",
  "layer": "architecture_decision",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/decision-index.json#/adrs/ADR-025",
    "generated/decision-index.json#/decisions/DEC-GOV-001",
    "generated/document-index.json",
    "contracts/system.contract.json#/active_documentation",
    "contracts/system.contract.json#/ai_boundary",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "contracts/ai-navigation.contract.json",
    "contracts/artifact-classes.contract.json",
    "schemas/test-evidence.schema.json"
  ],
  "decision_ids": [
    "DEC-GOV-001",
    "DEC-SYS-001",
    "DEC-PROFILE-001",
    "DEC-DATA-001",
    "DEC-REL-001",
    "DEC-AI-001"
  ],
  "requirement_ids": [
    "REQ-CONST-PRIN-001",
    "REQ-CONST-PRIN-002",
    "REQ-CONST-PRIN-007",
    "REQ-CONST-PRIN-009",
    "REQ-CONST-PRIN-010",
    "REQ-CONST-PRIN-013",
    "REQ-CONST-PRIN-014",
    "REQ-CONST-PRIN-017",
    "REQ-CONST-PRIN-018",
    "REQ-DEV-BTV-010",
    "REQ-DEV-BTV-019",
    "REQ-DEV-BTV-020",
    "REQ-DEV-BTV-021",
    "REQ-DEV-BTV-023",
    "REQ-DEV-BTV-024",
    "REQ-CONF-GEN-015",
    "REQ-CONF-GEN-019",
    "REQ-CONF-GEN-020",
    "REQ-CONF-GEN-021",
    "REQ-CONF-GEN-022",
    "REQ-CONF-GEN-023",
    "REQ-CONF-GEN-024",
    "REQ-LIFE-CAD-018",
    "REQ-LIFE-CAD-021"
  ],
  "lock_ids": [
    "LOCK-SYS-001",
    "LOCK-SYS-002",
    "LOCK-SYS-003",
    "LOCK-SYS-004",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-GOV-001",
    "DOC-GOV-002",
    "DOC-GOV-005",
    "DOC-GOV-006",
    "DOC-GOV-009",
    "DOC-GOV-010",
    "DOC-GOV-011",
    "DOC-GOV-012",
    "DOC-GOV-013",
    "DOC-GOV-014",
    "DOC-GOV-016",
    "DOC-CONST-003",
    "DOC-DEV-014",
    "DOC-LIFE-017",
    "DOC-CONF-012",
    "DOC-CONF-019"
  ],
  "tags": [
    "architecture-decision",
    "documentation-governance",
    "english-only",
    "active-corpus",
    "canonical-language",
    "translations",
    "localization",
    "generated-content",
    "validation",
    "migration",
    "ai-context",
    "non-authoritative-views"
  ]
}
KOA:DOC-META:END -->

# ADR-025 — English-Only Active Documentation

**ADR ID:** `ADR-025`  
**Status:** `accepted`  
**Decision class:** `major`  
**Decision owner:** `documentation_governance_authority`  
**Owner decision:** `DEC-GOV-001`  
**Change packet:** `CHG-2026-0025`  
**Created:** `2026-08-03`  
**Accepted:** `2026-08-03`  
**Effective:** `2026-08-03`  
**Supersedes:** Not applicable.  
**Superseded by:** Not applicable.

## 1. Decision Summary

All active authoritative kOA documentation uses English as its canonical language. Active Markdown, ADRs, registries, contracts, schema descriptions, generated projections, test catalogs, evidence summaries, migration records, release documentation, conformance material, and authoritative AI context packages declare language `en` and express controlling semantics in English.

Translations and localized explanations are permitted when they improve access, migration, operator comprehension, community participation, or user support. They remain version-bound non-authoritative views of an exact English source revision. Each view identifies target language, source identity, source revision, translation state, reviewer, omissions, terminology profile, drift state, and non-authority notice.

deprecated documents and source-language material can be preserved in archives, migration records, quotations, examples, evidence attachments, or language-artifact repositories. Presence in the repository does not create active authority.

## 2. Scope

### 2.1 Included scope

- Active documentation under `docs/`.
- Normative Markdown and ADRs.
- Decision, requirement, lock, traceability, test, evidence, schema, component, profile, release, artifact, migration, and integration registries.
- Schema and contract titles, descriptions, examples, comments, and kOA-owned validation messages.
- Generated projections, indexes, matrices, navigation, reports, and AI context packages.
- Active runbooks, security procedures, recovery instructions, and release gates.
- Language metadata, prose classification, translation lineage, drift detection, and migration.
- Optional translations, terminology packages, and source-language attachments.

### 2.2 Excluded scope

- Source-code identifiers, language keywords, commands, paths, URIs, filenames, schema keywords, and protocol values.
- User-generated content.
- Component-owned linguistic data and compiled language artifacts.
- Localized runtime interface strings.
- External evidence retained in its original language.
- Proper nouns, personal names, cultural names, registered marks, and titles that require preservation.
- Historical archive material outside the active corpus.
- A requirement that contributors, operators, users, or communities communicate only in English.
- A requirement that runtime interfaces use English.
- A required translation or localization implementation.

### 2.3 Active boundary

An artifact is active when the documentation registry assigns an active state and the artifact participates in current architecture, governance, implementation, operations, security, release, conformance, migration, or authoritative AI context.

The deprecated `doc/` root is archive or migration input only. The active canonical root is `docs/`.

## 3. Canonical References

### 3.1 Owner decision

- `generated/decision-index.json#/decisions/DEC-GOV-001`
- `DEC-GOV-001`

### 3.2 Canonical objects

- `generated/decision-index.json#/adrs/ADR-025`
- `generated/document-index.json`
- `contracts/system.contract.json#/active_documentation`
- `generated/requirements-index.json`
- `generated/assertion-index.json`
- `generated/traceability.json`
- `generated/test-catalog.json`
- `generated/evidence-catalog.json`
- `contracts/renderers.registry.json`
- `contracts/schemas.registry.json`

### 3.3 Related decisions

- `DEC-GOV-001`
- `DEC-SYS-001`
- `DEC-PROFILE-001`
- `DEC-DATA-001`
- `DEC-REL-001`
- `DEC-AI-001`

### 3.4 Related requirements

- `REQ-CONST-PRIN-001`
- `REQ-CONST-PRIN-002`
- `REQ-CONST-PRIN-007`
- `REQ-CONST-PRIN-009`
- `REQ-CONST-PRIN-010`
- `REQ-CONST-PRIN-013`
- `REQ-CONST-PRIN-014`
- `REQ-CONST-PRIN-017`
- `REQ-CONST-PRIN-018`
- `REQ-DEV-BTV-010`
- `REQ-DEV-BTV-019`
- `REQ-DEV-BTV-020`
- `REQ-DEV-BTV-021`
- `REQ-DEV-BTV-023`
- `REQ-DEV-BTV-024`
- `REQ-CONF-GEN-015`
- `REQ-CONF-GEN-019`
- `REQ-CONF-GEN-020`
- `REQ-CONF-GEN-021`
- `REQ-CONF-GEN-022`
- `REQ-CONF-GEN-023`
- `REQ-CONF-GEN-024`
- `REQ-LIFE-CAD-018`
- `REQ-LIFE-CAD-021`

### 3.5 Related locks

- `LOCK-SYS-001`
- `LOCK-SYS-002`
- `LOCK-SYS-003`
- `LOCK-SYS-004`
- `LOCK-PROFILE-001`
- `LOCK-PROFILE-002`
- `LOCK-DATA-001`
- `LOCK-GOV-001`
- `LOCK-COMP-001`
- `LOCK-COMP-002`
- `LOCK-LIFE-001`
- `LOCK-LIFE-002`
- `LOCK-LIFE-003`
- `LOCK-LIFE-004`
- `LOCK-AI-001`
- `LOCK-AI-002`
- `LOCK-IMPL-001`
- `LOCK-IMPL-002`

### 3.6 Related exceptions

Not applicable.

## 4. Context and Problem

### 4.1 Current state

The active corpus already uses English metadata and prose. Static validation includes English-only active content. Normative documents validate that active prose is English. Generated-content validation requires metadata agreement, deterministic rendering, and locale-independent output.

The broader migration corpus contains deprecated documents, historical titles, source quotations, language artifacts, and multilingual user needs. Those materials require preservation and sometimes translation without becoming competing authority.

### 4.2 Problem statement

When several language versions are simultaneously authoritative, differences can arise in normative force, negation, scope, exceptions, component ownership, profile membership, security conditions, lifecycle, compatibility, consent, cultural authority, recovery, and validation.

Even reviewed translations can lag behind source changes. Unreviewed machine translation can alter small words with large architectural consequences. Bilingual files can drift paragraph by paragraph.

### 4.3 Why an ADR is required

Language affects decisions, requirements, locks, contracts, procedures, evidence, release gates, and incident instructions. The system needs one controlling wording and one correction path while supporting multilingual access.

### 4.4 Constraints

- One canonical active language.
- Controlled translations remain possible.
- Source-language evidence and authentic names remain preservable.
- Generated content remains deterministic and locale-independent.
- Validators distinguish prose from technical tokens.
- deprecated material remains historically reconstructable.
- Offline bundles can include translations without promoting them.
- AI output remains candidate material.
- Corrections occur in the English source and propagate through impact analysis.
- High-impact translations receive qualified review.

## 5. Decision Drivers

1. One authoritative semantic baseline.
2. Exact requirement and decision wording.
3. Deterministic generated content.
4. Reduced translation drift.
5. Simpler review and traceability.
6. Clear deprecation and supersession.
7. Reliable security and recovery instructions.
8. Stable AI context packages.
9. Multilingual accessibility.
10. Preservation of original evidence and cultural terms.
11. Transparent translation status.
12. Implementation-neutral tooling.
13. Clear authority boundaries.
14. Offline distribution of reviewed translations.

## 6. Considered Options

| Option | Model | Decision | Rationale |
| --- | --- | --- | --- |
| `A` | One English authoritative corpus with version-bound translations | `Selected` | One semantic baseline with multilingual access. |
| `B` | Fully multilingual active normative corpus | `Rejected` | Creates competing controlling phrasings and high synchronization cost. |
| `C` | Bilingual prose in every active document | `Rejected` | Creates paragraph-level drift and doubles review and generated surfaces. |
| `D` | English identifiers with unrestricted active prose languages | `Rejected` | Identifiers alone do not prevent semantic divergence. |
| `E` | Automatic machine translation as active publication | `Rejected` | Unreviewed translation can alter force, scope, negation, and exceptions. |
| `F` | No translations | `Rejected` | Blocks accessibility and community participation unnecessarily. |

### 6.1 Selected model

The English corpus is the sole active semantic authority. A translation is a dependent artifact and can be operationally useful, but disputes, conformance, release, architecture closure, and source correction resolve against its exact English source.

### 6.2 Accessibility without co-authority

A version-bound translation with source linkage, review, terminology, and visible drift state provides access without creating a second place where system semantics can change.

## 7. Decision

### 7.1 Selected architecture

`english_canonical_active_corpus_with_version_bound_non_authoritative_translations`

### 7.2 Active-language rule

Every active documentation artifact declares `language: en` or its schema equivalent.

| Content class | Language | Active rule | Treatment |
| --- | --- | --- | --- |
| Normative Markdown | English | Required | All controlling prose and validation criteria. |
| ADR | English | Required | Decision context, options, consequences, migration, and record. |
| Canonical registry | English descriptions | Required | Identifiers remain exact machine values. |
| Schema and contract | English descriptions | Required | Titles, descriptions, examples, comments, and owned errors. |
| Generated projection | English | Required | Inherits canonical source language and fixed renderer locale. |
| Test and evidence | English | Required | Assertions, results, reasons, validity, and traceability. |
| Migration record | English | Required when active | May quote non-authoritative source material with English disposition. |
| AI context package | English | Required when authoritative | Source-language excerpts require English framing. |
| Translation view | Target language | Non-authoritative | Must identify exact English source revision and drift state. |
| deprecated archive | Preserved source language | Historical only | Excluded from active authority. |

### 7.3 Canonical wording


Corrections use ordinary ownership, decision, review, impact, regeneration, test, and evidence workflows.

### 7.4 Permitted non-English material

| Case | Required treatment |
| --- | --- |
| Proper noun or authentic community name | Preserve exact form and provide English context when meaning matters. |
| Identifier, command, path, URI, schema keyword, or artifact name | Preserve exact machine value. |
| Source quotation | Mark as quotation, cite it, and provide sufficient English explanation. |
| Non-normative user example | Label as example and describe the relevant behavior in English. |
| deprecated filename or historical title | Preserve for lineage and pair with an English disposition. |
| Language artifact or linguistic data | Store under its owning artifact contract rather than as active prose. |
| Localized user-interface string | Manage as a localization artifact outside canonical documentation. |

A permitted fragment cannot create a hidden normative clause.

### 7.5 Translation contract

Each translation records:

- translation artifact ID;
- target language and locale;
- exact English source document ID;
- immutable source revision;
- translation state;
- translator or process identity;
- reviewer when required;
- terminology profile;
- included and omitted sections;
- deviations or notes;
- validation tests and evidence;
- invalidation conditions;
- non-authority notice;
- replacement lineage.

### 7.6 Translation states

| State | Entry condition | Effect |
| --- | --- | --- |
| `requested` | Audience and exact English source identified. | No translated content is current. |
| `in_translation` | Work is underway from a fixed source revision. | Incomplete and non-authoritative. |
| `reviewed` | Terminology, omissions, and material meaning checked. | Can be distributed with non-authority notice. |
| `current` | Reviewed view matches the declared source revision. | Useful view, never canonical authority. |
| `stale` | English source changed materially. | Warning required; cannot support active claims. |
| `superseded` | A newer translation replaces it. | Historical lineage retained. |
| `archived` | Retained for history, migration, or research. | Excluded from current navigation. |

### 7.7 High-impact translations

Security, identity, trust, privilege, consent, disclosure, cultural-rights, legal, retention, deletion, incident, recovery, activation, rollback, conformance, and release translations require qualified review appropriate to the subject.

### 7.8 Registry and navigation

The documentation registry distinguishes English authority, current translation, stale translation, superseded translation, archived translation, and non-authoritative source.

Active indexes and authoritative AI contexts resolve references to English documents. Translation indexes display language, source revision, state, review, and warnings.

### 7.9 Generated content

Active renderers use fixed English output, fixed locale, fixed Unicode normalization, fixed line endings, and deterministic ordering.

Host locale does not alter headings, labels, booleans, dates, sorting, punctuation, validation messages, or generated requirement wording.

Localized renderers use separate non-authoritative output contracts.

### 7.10 External evidence

External tool output can remain in its original language. The evidence package preserves original bytes and adds English classification, context, result, expected result, and explanation sufficient for the active claim.

### 7.11 Authority boundary

A translation cannot substitute for the English source in decision closure, normative reference, conformance, release approval, security authorization, policy decision, evidence validity, migration authority, or generated-source resolution.

### 7.12 AI boundary

AI-assisted translation is candidate content only. AI cannot approve, mark current, resolve terminology disputes, publish as authority, validate high-impact equivalence, replace qualified review, or modify the English source automatically.

## 8. Canonical Ownership and Data Boundaries

### 8.1 Owners

- ADR owner: `generated/decision-index.json#/adrs/ADR-025`
- Decision owner: `generated/decision-index.json#/decisions/DEC-GOV-001`
- Active corpus owner: `generated/document-index.json`
- Translation lifecycle owner: documentation governance

### 8.2 Source ownership

Each active document retains its semantic owner. This ADR owns the language and authority relationship; it does not take over component, profile, security, policy, release, or data semantics.

### 8.3 Translation ownership

A translation owns its wording, terminology notes, review state, and drift metadata. It does not own the source decision or requirement.

### 8.4 Rights and provenance

Translation preserves attribution, provenance, consent, cultural authority, disclosure restrictions, and authentic names. A term with no safe equivalent remains in its authentic form with English explanation.

### 8.5 Write boundary

Translation workflows write translation artifacts, terminology records, review records, drift state, and evidence. They modify English sources only through ordinary source governance.

### 8.6 Reference boundary

Active references point to English source IDs. Interfaces can select a translation through an explicit source-to-view relationship and preserve a route to the source.

### 8.7 deprecated boundary

non-authoritative source-language documents retain original bytes, titles, paths, and provenance. Migration creates English active replacements without overwriting historical sources.

## 9. Profile and Deployment Effects

| Profile or overlay | Permitted support | Authority boundary |
| --- | --- | --- |
| `user_lightweight` | Localized help can be installed as a non-authoritative view. | Conformance references English sources. |
| `developer_linux_workstation` | Contributors may draft locally in another language. | Active pull-request documentation becomes English. |
| `developer_windows_wsl` | Localized onboarding can be packaged separately. | WSL does not change documentation authority. |
| `sovereign_linux_node` | Reviewed operator translations may be distributed. | Security and recovery authority remains English. |
| `sovereign_hub` | Community-facing views may be multilingual. | Multi-community operation does not create multiple canonical corpora. |
| `build_farm` | External tool output may remain in its original language. | Evidence conclusions and pass criteria remain English. |
| `control_plane` | Operator interfaces can localize display text. | Fleet semantics and receipts resolve to English sources. |
| `high_assurance` | Can strengthen legal, security, and qualified translation review. | Cannot add a second authoritative language. |
| `sovereign_offline` | Offline bundles can include current translations. | They retain exact English source revisions. |
| `appliance_shell` | The shell can present localized guidance. | Localization remains separate from canonical documentation. |

### 9.1 Packaging

Profiles and offline bundles can package translations, terminology, review evidence, and translation indexes. Package presence does not create authority.

### 9.2 Localized interfaces

Localized interfaces can display summaries, help, navigation, status explanations, warnings, and operator guidance. Canonical IDs, machine codes, source revision, translation state, and an English-source link remain available.

## 10. Security, Privacy, Rights, and AI Effects

### 10.1 Security

One controlling language reduces inconsistent interpretation of privilege, denial conditions, break-glass, signer scope, trust, revocation, incident severity, recovery, and authorization.

Stable identifiers and error codes are not translated.

### 10.2 Privacy

Translation workflows receive only content authorized for that purpose. Secrets, personal data, unpublished security details, and restricted evidence are excluded unless explicit authorization permits processing.

### 10.3 Cultural rights

English authority is not permission to erase or Anglicize authentic names. Community and cultural terms preserve authoritative forms, provenance, consent, and explanatory notes.

### 10.4 Legal and consent material

Local law or accessibility obligations can require reviewed localized notices or agreements. Those operational artifacts remain linked to English architecture authority and their own legal or consent owner.

### 10.5 AI

This decision introduces no native AI translation authority. External AI output remains candidate material and cannot establish equivalence merely through semantic similarity.

## 11. Offline, Resource, and Operational Effects

### 11.1 Offline behavior

Offline deployments retain the English corpus and packaged translations. A disconnected translation remains tied to its packaged source revision and cannot claim synchronization with a newer source.

Signed offline bundles can carry English documents, translations, terminology, review evidence, and drift metadata.

### 11.2 Resources

Resource Governor can bound corpus scans, language detection, translation, terminology checks, comparison, localized rendering, logs, and evidence. Resource pressure can defer translation work but not required active-corpus validation.

### 11.3 Contributor workflow

A contributor may draft in another language outside the active corpus. Before activation, a reviewed English proposal enters the ordinary governance workflow. The original draft can remain attached as provenance.

### 11.4 Translation workflow

1. Select the exact English source revision.
2. classify audience and impact;
3. select terminology and review requirements;
4. create the translation;
5. preserve IDs, code, and links;
6. validate structure and omissions;
7. compare normative force;
8. obtain required review;
9. register evidence;
10. mark current only for that source revision;
11. monitor source impact.

### 11.5 Failure matrix

| Failure state | Required response | Preserved state | Blocked behavior |
| --- | --- | --- | --- |
| Active metadata language is not `en` | Fail active-corpus validation. | Last valid English document | Non-English active authority |
| Material non-English prose is unclassified | Require English wording or explicit non-authoritative treatment. | Permitted identifiers and quotations | Implicit second authority |
| Translation lacks exact source revision | Mark invalid or historical. | English source | Current-translation claim |
| English source changes materially | Mark dependent translations stale. | Prior translation as history | Silent current status |
| Translation changes normative force | Reject and require correction and review. | English controlling statement | Translation-based conformance |
| Generated output depends on locale | Fail renderer validation. | Last validated projection | Locale-dependent active bytes |
| External evidence is non-English | Preserve original and add English classification and explanation. | Original evidence integrity | Unexplained result |
| deprecated document appears as active | Migrate, translate, or archive before activation. | deprecated bytes and provenance | Implicit active status |
| Translation provider is unavailable | Leave view absent or stale. | English corpus | Silent provider substitution |
| Review evidence is invalidated | Downgrade translation state. | Historical translation | Current-view claim |
| Language detector is uncertain | Require explicit human classification. | Last valid corpus | Guessing by majority language |
| English wording is ambiguous | Correct the English source through governance. | Decision history | Translation override |
| Localized emergency instruction conflicts | Withdraw it and use canonical procedure. | English recovery source | Local reinterpretation |
| AI produces a translation | Treat it as candidate content requiring review. | Canonical source | Automatic authoritative publication |

## 12. Compatibility and Lifecycle

### 12.1 Compatibility class

`compatible_with_migration`

The decision matches the active English corpus and requires migration for any active non-English or mixed-language authority.

### 12.2 Document compatibility

An active document is language-compatible when metadata declares `en`, controlling prose is English, permitted fragments are classified, generated output is locale-independent, references resolve, and no translation claims authority.

### 12.3 Translation compatibility

A translation is compatible only with its exact source revision, declared included sections, terminology profile, audience, locale, review state, and validity conditions.

### 12.4 Supersession

When an English source is superseded, translations become stale, superseded, or historical until replacements bind to the new source. Redirects do not imply semantic equivalence automatically.

### 12.5 Deprecation and archival

Translations can be deprecated independently. Removal occurs only after dependency, retention, legal, rights, migration, audit, offline, and historical-reconstruction obligations.

### 12.6 Identifiers

Document, decision, requirement, lock, test, evidence, profile, component, artifact, and release identifiers are not translated. Translation artifacts receive separate IDs.

### 12.7 Versioning

A material English wording change creates a new source revision and invalidates dependent current-translation claims. Translation corrections create translation revisions without changing the source.

## 13. Migration Plan

### 13.1 Preconditions

- Accepted `DEC-GOV-001`.
- Active documentation registry.
- Active-root and archive-root definitions.
- Language validator with classification rules.
- Translation lifecycle model.
- Source-to-translation traceability.
- Qualified-review policy.
- Generated-content locale controls.
- Migration inventory.

### 13.2 Inventory

Record path, document ID, state, declared language, observed language, class, owner, generated regions, non-authoritative source, translations, references, rights, retention, and disposition.

### 13.3 Classification

Each artifact becomes active English authority, English replacement required, current translation, stale translation, source-language evidence, language artifact, localized runtime content, migration-only deprecated, historical archive, or obsolete content for disposition.

### 13.4 Convert active non-English content

1. Preserve original bytes and provenance.
2. identify owner and current semantics;
3. produce an English candidate;
4. resolve ambiguity with the owner;
5. preserve authentic names;
6. review decisions, requirements, scope, and exceptions;
7. register the English document;
8. update references and projections;
9. create optional translation views;
10. archive the original with lineage;
11. run impact and validation.

### 13.5 Convert mixed-language documents

Separate English canonical prose, permitted quotations or examples, translation notes, attached source-language material, and localized runtime artifacts. Unclassified mixed normative prose is removed from the active version.

### 13.6 Migrate translations

Identify source and revision, assess completeness and drift, assign state, add non-authority notice, record reviewer and terminology, validate links and IDs, and archive views whose source relationship cannot be established.

### 13.7 Migrate generated content

Active renderers receive explicit English output contracts. Locale-dependent outputs are regenerated. Localized renderers are registered separately.

### 13.8 deprecated disposition

- Active root: `docs/`.
- deprecated root: `doc/`.
- deprecated non-English documents remain migration inputs or archives.
- Original paths and titles remain in lineage.
- Redirects point to English replacements only when mapping is valid.
- Historical bytes are not rewritten merely to satisfy active rules.

### 13.9 Cutover

Cutover completes when every active document declares `en`, active prose passes validation, non-English candidates have final disposition, translations have source revisions and states, active indexes resolve English authority, generated content is locale-independent, and evidence passes.

## 14. Rollback and Forward Repair

### 14.1 Rollback unit


### 14.2 Rollback triggers

- English conversion changes meaning incorrectly.
- Requirement or decision force is lost.
- Source lineage is missing.
- Translation is promoted accidentally.
- Generated output becomes locale-dependent.
- High-impact terminology is incorrect.
- References point to stale views as authority.
- Active non-English content remains undisclosed.

### 14.3 Rollback procedure

1. Stop activation.
2. preserve failed candidates;
3. restore previous registry and English corpus;
4. restore mappings and navigation;
5. invalidate affected evidence;
6. correct source, renderer, validator, migration, or translation;
7. rerun impact and validation;
8. reactivate after passing evidence.

### 14.4 Forward repair

Forward repair produces a corrected English source or translation revision. A translation cannot repair an ambiguous source by becoming authoritative.

### 14.5 Missing lineage

A useful translation without provable source revision remains historical. A new translation is produced from a verified English source when needed.

## 15. Interfile Alignment Impact

### 15.1 Impact report

- `generated/impact/IMPACT-2026-08-03-ADR-025.json`

### 15.2 Modified or constrained objects

- `generated/decision-index.json#/adrs/ADR-025`
- `generated/document-index.json`
- `contracts/system.contract.json#/active_documentation`
- `contracts/renderers.registry.json`
- `generated/test-catalog.json#/tests/TEST-ADR-025-001`
- `generated/traceability.json#/adrs/ADR-025`

### 15.3 Affected documents

| Document ID | Disposition | Reason |
| --- | --- | --- |
| `DOC-CONST-003` | `reviewed_no_change` | Already validates English active prose. |
| `DOC-DEV-014` | `updated` | Static validation includes active-corpus language checks. |
| `DOC-LIFE-017` | `updated` | Translation lifecycle uses compatibility and supersession. |
| `DOC-CONF-012` | `updated` | Generated active content inherits English and rejects locale drift. |
| `DOC-CONF-019` | `updated` | Gates require active language evidence. |
| `DOC-GOV-000` | `updated` | Documentation governance identifies canonical language. |
| `DOC-GOV-016` | `updated` | Migration classifies deprecated and translated material. |

### 15.4 Affected locks

| Lock ID | Disposition | Effect |
| --- | --- | --- |
| `LOCK-SYS-001` | `unchanged` | Supports one explicit active authority. |
| `LOCK-SYS-002` | `unchanged` | Offline access can include translations without changing authority. |
| `LOCK-PROFILE-001` | `unchanged` | Packaged translations remain profile-scoped. |
| `LOCK-DATA-001` | `unchanged` | Translation does not transfer data ownership. |
| `LOCK-GOV-001` | `unchanged` | Documentation governance owns language lifecycle. |
| `LOCK-COMP-001` | `unchanged` | Components retain one canonical semantic contract. |
| `LOCK-LIFE-001` | `unchanged` | Documents and translations retain lifecycle and lineage. |
| `LOCK-LIFE-004` | `unchanged` | Source changes invalidate dependent views safely. |
| `LOCK-AI-001` | `unchanged` | No native AI translation authority. |
| `LOCK-AI-002` | `unchanged` | External AI remains candidate input. |
| `LOCK-IMPL-001` | `unchanged` | Tooling remains replaceable. |
| `LOCK-IMPL-002` | `unchanged` | No localization platform becomes universal. |

### 15.5 Affected requirements

| Requirement ID | Disposition | Effect |
| --- | --- | --- |
| `REQ-DEV-BTV-010` | `unchanged` | Static validation includes language checks. |
| `REQ-DEV-BTV-019` | `unchanged` | Evidence uses the registered schema. |
| `REQ-DEV-BTV-021` | `unchanged` | Source changes trigger evidence review. |
| `REQ-CONF-GEN-015` | `unchanged` | Generated metadata agrees on language. |
| `REQ-CONF-GEN-019` | `unchanged` | References resolve to correct lifecycle states. |
| `REQ-CONF-GEN-020` | `unchanged` | Language changes trigger impact analysis. |
| `REQ-CONF-GEN-021` | `unchanged` | Superseded sources invalidate dependent views. |
| `REQ-CONF-GEN-023` | `unchanged` | AI cannot become authoritative generated content. |
| `REQ-LIFE-CAD-018` | `unchanged` | Supersession preserves translation lineage. |
| `REQ-LIFE-CAD-021` | `unchanged` | Material changes trigger cross-corpus impact. |

### 15.6 Generated artifacts


## 16. Validation and Evidence

### 16.1 Required tests

| Test ID | Purpose | Required result |
| --- | --- | --- |
| `TEST-ADR-025-001` | Active artifacts declare language `en` and resolve in the documentation registry. | `pass` |
| `TEST-ADR-025-002` | English prose validation excludes code, identifiers, paths, URIs, proper nouns, and classified quotations. | `pass` |
| `TEST-ADR-025-003` | Normative decisions, requirements, procedures, failures, and validation criteria have one English wording. | `pass` |
| `TEST-ADR-025-004` | Generated active projections inherit English and remain locale-independent. | `pass` |
| `TEST-ADR-025-005` | Registry, contract, schema, test, evidence, and owned error descriptions follow language rules. | `pass` |
| `TEST-ADR-025-006` | Each translation records source revision, target language, state, reviewer, omissions, and non-authority. | `pass` |
| `TEST-ADR-025-007` | Material source changes propagate stale state to dependent translations. | `pass` |
| `TEST-ADR-025-008` | Translations cannot replace English sources in normative, release, security, or conformance references. | `pass` |
| `TEST-ADR-025-009` | Permitted source-language names, quotations, examples, and language artifacts retain English framing. | `pass` |
| `TEST-ADR-025-010` | Active-root and deprecated-archive separation is complete. | `pass` |
| `TEST-ADR-025-011` | Non-English external evidence receives English classification without altering original bytes. | `pass` |
| `TEST-ADR-025-012` | Profiles, overlays, offline bundles, UI localization, and documentation authority remain separate. | `pass` |
| `TEST-ADR-025-013` | High-impact translations receive required terminology and qualified review. | `pass` |
| `TEST-ADR-025-014` | Current, stale, superseded, and archived translation lifecycle is enforced. | `pass` |
| `TEST-ADR-025-015` | Sorting, dates, generated wording, and validation results are independent of host locale. | `pass` |
| `TEST-ADR-025-016` | Migration preserves original source language, provenance, redirects, and historical reconstruction. | `pass` |
| `TEST-ADR-025-017` | Native and external AI have no translation approval or publication authority. | `pass` |
| `TEST-ADR-025-018` | ADR, registry, documents, translations, tests, evidence, impact, and context traceability is complete. | `pass` |

### 16.2 Required evidence

| Evidence ID | Evidence type | Location |
| --- | --- | --- |
| `EVID-ADR-025-CORPUS` | Active-corpus language and metadata report | `generated/evidence-catalog.json#/evidence/EVID-ADR-025-CORPUS` |
| `EVID-ADR-025-TRANSLATIONS` | Translation inventory, source lineage, lifecycle, and drift report | `generated/evidence-catalog.json#/evidence/EVID-ADR-025-TRANSLATIONS` |
| `EVID-ADR-025-MIGRATION` | deprecated-language migration, archive, redirect, and disposition evidence | `generated/evidence-catalog.json#/evidence/EVID-ADR-025-MIGRATION` |
| `EVID-ADR-025-REVIEW` | Qualified terminology and high-impact translation review evidence | `generated/evidence-catalog.json#/evidence/EVID-ADR-025-REVIEW` |
| `EVID-ADR-025-GENERATION` | Locale-independent generated-content validation evidence | `generated/evidence-catalog.json#/evidence/EVID-ADR-025-GENERATION` |
| `EVID-ADR-025-AUTHORITY` | Canonical-source and non-authoritative-view boundary report | `generated/evidence-catalog.json#/evidence/EVID-ADR-025-AUTHORITY` |

### 16.3 Validation commands

```bash
python docs/tools/generate_docs.py --check
python docs/tools/check_normative_language.py
python docs/tools/check_language.py
python docs/tools/check_active_english.py
python docs/tools/check_translation_lineage.py
python docs/tools/check_translation_drift.py
python docs/tools/check_canonical_ownership.py
python docs/tools/check_generated_content.py
python docs/tools/check_document_graph.py
python docs/tools/check_traceability.py
python docs/tools/check_decision_closure.py
python docs/tools/check_no_unresolved_state.py
python docs/tools/compute_impact.py --check-clean
python docs/tools/build_ai_context.py --check
python docs/tools/check_clean_repository.py
python docs/tools/validate_docs.py
```

### 16.4 Validator behavior

The validator reads metadata, distinguishes prose from code and identifiers, recognizes classified quotations and examples, reports exact ranges, requires human classification for uncertain regions, does not rewrite content, and records its version and configuration.

### 16.5 Acceptance criteria

1. Every active document declares `en`.
2. Every active controlling statement is English.
3. Permitted non-English material is classified and framed.
4. Active references resolve to English authority.
5. Every translation has exact source revision and non-authority notice.
6. Source changes mark dependent translations stale.
7. Generated active content is locale-independent.
8. non-authoritative content has final disposition.
9. High-impact translations have required review.
10. Original source-language evidence remains intact.
11. AI has no translation authority.
12. All affected objects have final dispositions.
13. All tests pass.
14. Evidence resolves and remains valid.

## 17. Consequences

### 17.1 Positive consequences

- One controlling semantic corpus.
- Clear dispute and correction path.
- Exact requirements and decisions.
- Simpler generated-content validation.
- Easier traceability.
- Lower translation-drift risk.
- Stable AI contexts.
- Clear archive boundaries.
- Multilingual access without competing authority.
- Better security and recovery review.
- Preserved authentic names and evidence.
- Replaceable tooling.

### 17.2 Negative consequences

- Non-English contributors need editorial or translation support.
- High-quality translations require maintenance.
- Views can become stale.
- English ambiguity can propagate.
- Validators can misclassify technical text.
- Terminology and review evidence add work.
- Local legal obligations can require extra localized artifacts.
- One canonical language can centralize editorial power without inclusive governance.

### 17.3 Participation obligations

Governance supports source-language proposals, translation assistance, bilingual issue discussion, preservation of original submissions, community review of significant terms, acknowledgement of translators, and transparent editorial changes.

English authority is not permission to exclude community expertise.

### 17.4 Operational obligations

Maintain language validation, translation inventory, drift detection, high-impact review, source evidence, offline packaging, visible translation state, UI separation, reviewer training, migration exercises, and historical lineage.

### 17.5 Documentation obligations

Keep this ADR, governance, migration, generated-content validation, build validation, conformance gates, registries, tests, and evidence aligned.

### 17.6 Accepted technical debt

The initial validator may combine deterministic structural rules, a bounded language detector, and human review for uncertain cases. Uncertain cases block rather than guess, and the validator cannot rewrite prose.

## 18. Rejected Alternatives

| Alternative | Reason rejected | Reconsideration trigger |
| --- | --- | --- |
| Fully multilingual active corpus | Multiple controlling wordings and high synchronization burden. | Formally verified force equivalence and sustainable qualified review. |
| Bilingual every-document format | Paragraph drift and doubled review surfaces. | Renderer-backed exact synchronized output without competing authority. |
| Unrestricted active prose languages | No single reviewable semantic baseline. | A different single canonical language is adopted through supersession. |
| Automatic translation as active content | Cannot guarantee normative force or high-impact meaning. | Deterministic formally validated translation accepted for defined domains. |
| English with no translations | Unnecessarily restricts access and participation. | None; controlled translations remain selected. |
| Translation overrides ambiguous source | Hides source defects and creates competing authority. | None; English source is corrected first. |
| Locale-dependent generated documentation | Different active bytes from one source. | Localized output remains separate and non-authoritative. |

## 19. Exceptions and Waivers

Not applicable.

A bounded exception can permit a specific non-English active operational notice when law, safety, accessibility, consent, or community authority requires it before an English paired record is complete.

The exception identifies exact artifact, language, audience, obligation, owner, English summary, authority scope, expiry, reviewer, migration plan, tests, and evidence.

It cannot create a permanent second normative corpus, alter canonical IDs, bypass ownership, authorize AI publication, or remove historical lineage.

## 20. Implementation Guidance

This section is non-normative.

A repository can organize translations and archives under registered paths such as:

```text
docs/
  10-adrs/
  09-conformance/
  translations/
    fr-CA/
    de/
    uk/
  archive/
  migration/
```

A translation manifest can include:

```json
{
  "translation_id": "TR-DOC-ADR-025-FR-CA-001",
  "source_doc_id": "DOC-ADR-025",
  "source_revision": "example-immutable-revision",
  "source_language": "en",
  "target_language": "fr-CA",
  "status": "current",
  "authoritative": false,
  "reviewer_refs": [
    "contracts/identities.registry.json#/reviewers/example-language-reviewer"
  ],
  "omitted_sections": [],
  "invalidation_conditions": [
    "material source change",
    "terminology profile change",
    "review evidence invalidation"
  ]
}
```

Language validation should parse Markdown structure rather than scan raw bytes indiscriminately.

Localized pages should display target language, translation state, source ID, source revision, last review, non-authority notice, source link, and stale warning.

## 21. Decision Record

### 21.1 Authority record

- Decision ID: `DEC-GOV-001`
- Decision status: `accepted`
- Decision owner: `documentation_governance_authority`
- Decision registry reference: `generated/decision-index.json#/decisions/DEC-GOV-001`
- Related system decision: `DEC-SYS-001`
- Related release decision: `DEC-REL-001`
- Related AI decision: `DEC-AI-001`

### 21.2 Review record

| Role | Identifier | Result | Date |
| --- | --- | --- | --- |
| Author | `documentation-migration-author` | `submitted` | `2026-08-03` |
| Canonical owner | `documentation-governance-authority` | `approved` | `2026-08-03` |
| Architecture reviewer | `architecture-governance` | `approved` | `2026-08-03` |
| Security reviewer | `security-authority` | `approved` | `2026-08-03` |
| Rights and terminology reviewer | `rights-and-language-review` | `approved` | `2026-08-03` |
| Validation pipeline | `automated` | `pass` | `2026-08-03` |
| Authority activator | `documentation-authority` | `activated` | `2026-08-03` |

### 21.3 Machine-readable change summary

```json
{
  "change_id": "CHG-2026-0025",
  "adr_ids": ["ADR-025"],
  "decision_ids": [
    "DEC-GOV-001",
    "DEC-SYS-001",
    "DEC-PROFILE-001",
    "DEC-DATA-001",
    "DEC-REL-001",
    "DEC-AI-001"
],
  "modified_canonical_refs": [
    "generated/decision-index.json#/adrs/ADR-025",
    "generated/document-index.json",
    "contracts/system.contract.json#/active_documentation",
    "contracts/renderers.registry.json"
  ],
  "requirement_ids": [
    "REQ-CONST-PRIN-001",
    "REQ-CONST-PRIN-002",
    "REQ-CONST-PRIN-007",
    "REQ-CONST-PRIN-009",
    "REQ-CONST-PRIN-010",
    "REQ-CONST-PRIN-013",
    "REQ-CONST-PRIN-014",
    "REQ-CONST-PRIN-017",
    "REQ-CONST-PRIN-018",
    "REQ-DEV-BTV-010",
    "REQ-DEV-BTV-019",
    "REQ-DEV-BTV-020",
    "REQ-DEV-BTV-021",
    "REQ-DEV-BTV-023",
    "REQ-DEV-BTV-024",
    "REQ-CONF-GEN-015",
    "REQ-CONF-GEN-019",
    "REQ-CONF-GEN-020",
    "REQ-CONF-GEN-021",
    "REQ-CONF-GEN-022",
    "REQ-CONF-GEN-023",
    "REQ-CONF-GEN-024",
    "REQ-LIFE-CAD-018",
    "REQ-LIFE-CAD-021"
],
  "lock_ids": [
    "LOCK-SYS-001",
    "LOCK-SYS-002",
    "LOCK-SYS-003",
    "LOCK-SYS-004",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002"
],
  "exception_ids": [],
  "test_ids": [
    "TEST-ADR-025-001",
    "TEST-ADR-025-002",
    "TEST-ADR-025-003",
    "TEST-ADR-025-004",
    "TEST-ADR-025-005",
    "TEST-ADR-025-006",
    "TEST-ADR-025-007",
    "TEST-ADR-025-008",
    "TEST-ADR-025-009",
    "TEST-ADR-025-010",
    "TEST-ADR-025-011",
    "TEST-ADR-025-012",
    "TEST-ADR-025-013",
    "TEST-ADR-025-014",
    "TEST-ADR-025-015",
    "TEST-ADR-025-016",
    "TEST-ADR-025-017",
    "TEST-ADR-025-018"
],
  "evidence_ids": [
    "EVID-ADR-025-CORPUS",
    "EVID-ADR-025-TRANSLATIONS",
    "EVID-ADR-025-MIGRATION",
    "EVID-ADR-025-REVIEW",
    "EVID-ADR-025-GENERATION",
    "EVID-ADR-025-AUTHORITY"
],
  "tests_run": [
    "metadata_parse",
    "adr_section_order",
    "active_english_language",
    "permitted_non_english_classification",
    "translation_lineage",
    "translation_drift",
    "generated_locale_independence",
    "legacy_archive_separation",
    "high_impact_translation_review",
    "no_ai_authority",
    "traceability",
    "no_unresolved_markers"
  ],
  "impact_report": "generated/impact/IMPACT-2026-08-03-ADR-025.json",
  "validation_status": "pass"
}
```

## 22. Supersession and Historical Integrity

When superseded:

1. status changes to `superseded`;
2. the replacement references `ADR-025`;
3. the original ID and path remain reserved;
4. English revisions, translations, source-language submissions, terminology, reviews, migration records, tests, evidence, and redirects remain according to retention;
5. active documents adopt the replacement language model only after complete migration;
6. old translations retain exact source revisions and historical states;
7. no replacement silently promotes a translation;
8. identifiers remain stable;
9. historical reconstruction can determine which wording governed each active period.

This ADR remains in the repository after acceptance, deprecation, rejection, or supersession.
