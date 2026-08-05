<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SYS-010",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "system",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/system.contract.json#/ai_boundary",
    "contracts/system.contract.json#/sentient_boundary",
    "contracts/system.contract.json#/ariane",
    "contracts/system.contract.json#/koa_mediatheque",
    "contracts/system.contract.json#/external_integrations",
    "contracts/integration-types.contract.json",
    "generated/profile-catalog.json",
    "generated/component-catalog.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-AI-001",
    "DEC-SENT-001",
    "DEC-MEDIATHEQUE-001",
    "DEC-UCKK-EXT-001",
    "DEC-ARI-001",
    "DEC-PROFILE-001",
    "DEC-DATA-001"
  ],
  "requirement_ids": [
    "REQ-SYS-EXTAI-001",
    "REQ-SYS-EXTAI-002",
    "REQ-SYS-EXTAI-003",
    "REQ-SYS-EXTAI-004",
    "REQ-SYS-EXTAI-005",
    "REQ-SYS-EXTAI-006",
    "REQ-SYS-EXTAI-007",
    "REQ-SYS-EXTAI-008",
    "REQ-SYS-EXTAI-009",
    "REQ-SYS-EXTAI-010",
    "REQ-SYS-EXTAI-011",
    "REQ-SYS-EXTAI-012",
    "REQ-SYS-EXTAI-013",
    "REQ-SYS-EXTAI-014",
    "REQ-SYS-EXTAI-015",
    "REQ-SYS-EXTAI-016",
    "REQ-SYS-EXTAI-017",
    "REQ-SYS-EXTAI-018",
    "REQ-SYS-EXTAI-019",
    "REQ-SYS-EXTAI-020"
  ],
  "lock_ids": [
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-SENT-001",
    "LOCK-MEDIATHEQUE-001",
    "LOCK-UCKK-EXT-001",
    "LOCK-ARI-001",
    "LOCK-ARI-002",
    "LOCK-DATA-001",
    "LOCK-PROFILE-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-UCKK-EXT-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-GOV-001",
    "DOC-GOV-002",
    "DOC-CONST-003",
    "DOC-SYS-000"
  ],
  "tags": [
    "system",
    "external-ai",
    "integrations",
    "chatgpt",
    "suno",
    "gamma",
    "ariane-voice",
    "candidate-input",
    "provenance",
    "offline-degradation"
  ]
}
KOA:DOC-META:END -->

# External AI Surfaces

## 1. Purpose

This document defines how kOA may use approved external AI-adjacent services without introducing native AI authority into the operating environment.

The global baseline remains deterministic and contains no native generative AI, classifier, summarizer, embedding model, autonomous routing model, autonomous agent, AI-generated category system, or AI-based ingestion decision. External services are optional, explicit, capability-scoped, removable surfaces whose outputs remain candidate inputs until accepted by an owning component.

This document governs ChatGPT, Suno, Gamma, and the approved Ariane voice adapter. It defines activation, data transfer, authority boundaries, controlled import, provenance, failure behavior, offline behavior, removal behavior, and local acceptance.

## 2. Scope

This document applies to:

- every user, developer, build, node, hub, or control-plane profile that permits an approved external surface;
- every component that exports data to or imports output from an approved external service;
- every user interface that initiates or reports an external operation;
- every integration adapter, gateway, receipt, provenance record, test, and evidence object associated with these surfaces;
- every online, restricted-network, intermittent, and offline transition affecting an approved external surface.

This document does not:

- authorize native AI in the global baseline;
- authorize services not registered in `contracts/integration-types.contract.json`;
- define provider-specific commercial terms or remote implementation internals;
- grant an external provider access to authoritative stores, secrets, tenant state, profile state, privilege, policy, releases, or publication;
- make SenTient an approved external AI surface;
- make external processing mandatory for any core capability.

SenTient remains a separate optional, isolated, non-authoritative research and enrichment workbench governed by its own component and profile contracts.

## 3. Canonical References

| Canonical reference | Ownership |
| --- | --- |
| `contracts/system.contract.json#/ai_boundary` | Native AI prohibition, approved external surfaces, and candidate-input rule |
| `contracts/system.contract.json#/sentient_boundary` | SenTient separation from the global baseline |
| `contracts/system.contract.json#/ariane` | Local navigation and optional external voice behavior |
| `contracts/system.contract.json#/koa_mediatheque` | Deterministic native kOA Mediatheque pipeline and external media-adapter workflow |
| `contracts/system.contract.json#/external_integrations` | Global external-integration requirements |
| `contracts/integration-types.contract.json#/policy` | Explicit allowlist, default authority, activation, transfer, and removal rules |
| `contracts/integrations/chatgpt.integration.json` | ChatGPT classification, capability scope, transfer, authority, provenance, failure, and removal |
| `contracts/integration-types.contract.json#/integrations/suno` | Suno classification, controlled media workflow, authority, provenance, failure, and removal |
| `contracts/integration-types.contract.json#/integrations/gamma` | Gamma classification, controlled presentation workflow, authority, provenance, failure, and removal |
| `contracts/integration-types.contract.json#/integrations/ariane_voice_adapter` | Voice-session activation, candidate intent, local validation, failure, and removal |
| `generated/profile-catalog.json#/external_integrations` | Profile-level availability and default enablement |
| `generated/component-catalog.json` | Owning component identity and authoritative data ownership |
| `generated/requirements-index.json` | Exact normative statements projected in Section 5 |
| `generated/assertion-index.json` | Cross-file AI, kOA Mediatheque, Ariane, data, profile, and lifecycle invariants |
| `generated/traceability.json` | Links among decisions, requirements, locks, components, profiles, tests, and evidence |
| `generated/test-catalog.json` | Registered conformance tests |
| `generated/evidence-catalog.json` | Registered evidence supporting conformance claims |

## 4. Model and Responsibilities

### 4.1 External-surface model

An external AI surface is a registered, optional integration that performs one declared external capability outside the kOA authoritative core.

Every operation follows this authority chain:

`text
explicit user action
 -> profile permission
 -> registered integration
 -> disclosed outbound data
 -> external processing
 -> candidate output
 -> local validation
 -> owning-component acceptance
 -> optional authoritative use or publication
`

The external service owns only remote processing. It does not own kOA data, policy, privilege, release, publication, or component authority.

### 4.2 Approved surfaces

| Integration | Classification | Authority class | Capability scope | Unavailable behavior |
| --- | --- | --- | --- | --- |
| `chatgpt` | `external_ai_assistance` | `non_authoritative_candidate_source` | user requested assistance, candidate text generation, candidate structured output, candidate analysis | The requested external assistance operation is unavailable; unrelated local capabilities remain operational. |
| `suno` | `external_media_generation` | `non_authoritative_candidate_source` | user requested audio generation, user requested music generation, candidate media artifact return | External media generation is unavailable; deterministic local kOA Mediatheque operations remain operational. |
| `gamma` | `external_presentation_generation` | `non_authoritative_candidate_source` | user requested presentation generation, candidate presentation artifact return | External presentation generation is unavailable; unrelated local capabilities remain operational. |
| `ariane_voice_adapter` | `external_voice_capability` | `non_authoritative_candidate_command_source` | voice input processing, candidate navigation intent return | Voice controls are unavailable; Ariane local keyboard, pointer, touch, menu, shortcut, and accessibility navigation remain operational. |

The allowlist is closed. A new provider or capability requires an accepted owner decision, a registered integration object, applicable profile rules, requirements, locks, tests, evidence, and activation through the authority registry.

### 4.3 Common responsibilities

The initiating interface shall:

- identify the external service and capability;
- disclose the data selected for transfer;
- require explicit user action;
- prevent background or automatic invocation;
- display success, failure, cancellation, and offline states.

The integration adapter shall:

- transfer only admitted data;
- prevent implicit repository or authoritative-store access;
- preserve provider and operation identity;
- return output as candidate material;
- fail without authoritative mutation.

The owning component shall:

- validate format, schema, content, authority, and policy;
- determine whether the output may be imported;
- record provenance when required;
- obtain user or policy acceptance;
- own the accepted local state;
- reject invalid, ambiguous, incompatible, or unauthorized output.

The publication path shall:

- remain separate from generation;
- require the applicable publication request, policy, gateway, and receipt;
- preserve provenance and rights constraints;
- never infer publication consent from generation or import.

### 4.4 ChatGPT responsibility

ChatGPT may provide user-requested candidate text, structured output, analysis, or assistance.

ChatGPT output:

- has no direct authority;
- cannot mutate component stores;
- cannot authorize actions;
- cannot activate releases;
- cannot publish content;
- becomes usable only through explicit local validation and acceptance.

No chat session, prompt, generated answer, or provider response is an owner decision unless the decision is recorded through the canonical decision process.

### 4.5 Suno and Gamma responsibility

Suno and Gamma are external generation adapters.

Their canonical workflow is:

1. explicit user selection;
2. controlled export;
3. external processing;
4. controlled re-import;
5. provenance receipt;
6. user approval;
7. optional publication.

They shall not be triggered by native ingestion, indexing, classification, routing, tagging, synchronization, or background enrichment.

Generated media or presentation artifacts remain candidate artifacts until admitted by an owning component.

### 4.6 Ariane external voice responsibility

Ariane external voice is an optional input surface. The external adapter returns a candidate navigation intent.

The Ariane Runtime retains authority to:

- validate the candidate against the active deterministic command set;
- reject unknown intent;
- reject ambiguous intent;
- request explicit confirmation;
- execute only profile-enabled local commands.

The external adapter cannot execute commands directly.

Local Ariane navigation remains independent of the external voice adapter.

### 4.7 SenTient separation

SenTient is not part of the four-surface external AI allowlist.

It is:

- an optional research and enrichment workbench;
- available only in approved development and build profiles;
- explicitly task-activated;
- isolated in dependencies, storage, identities, temporary data, networking, CPU, and memory;
- non-authoritative;
- prohibited from direct writes to another component's authoritative store.

SenTient output uses controlled import and component acceptance, but its lifecycle and isolation remain component and profile concerns rather than external-provider integration concerns.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-SYS-EXTAI-001,REQ-SYS-EXTAI-002,REQ-SYS-EXTAI-003,REQ-SYS-EXTAI-004,REQ-SYS-EXTAI-005,REQ-SYS-EXTAI-006,REQ-SYS-EXTAI-007,REQ-SYS-EXTAI-008,REQ-SYS-EXTAI-009,REQ-SYS-EXTAI-010,REQ-SYS-EXTAI-011,REQ-SYS-EXTAI-012,REQ-SYS-EXTAI-013,REQ-SYS-EXTAI-014,REQ-SYS-EXTAI-015,REQ-SYS-EXTAI-016,REQ-SYS-EXTAI-017,REQ-SYS-EXTAI-018,REQ-SYS-EXTAI-019,REQ-SYS-EXTAI-020 -->
- **REQ-SYS-EXTAI-001 — SHALL:** The active external AI allowlist shall contain only ChatGPT, Suno, Gamma, and the approved Ariane voice adapter.
- **REQ-SYS-EXTAI-002 — SHALL NOT:** An unregistered AI, media-generation, presentation-generation, voice, classification, summarization, embedding, routing, or agent service shall not be invoked by an active kOA workflow.
- **REQ-SYS-EXTAI-003 — SHALL:** Every external AI operation shall be explicitly initiated by a user for one declared capability.
- **REQ-SYS-EXTAI-004 — SHALL:** The system shall disclose the data selected for transfer before an external operation begins.
- **REQ-SYS-EXTAI-005 — SHALL:** Only data explicitly admitted for the current operation shall be transferred to the external service.
- **REQ-SYS-EXTAI-006 — SHALL NOT:** An external integration shall not receive implicit repository, component-store, tenant, profile, secret, or host access.
- **REQ-SYS-EXTAI-007 — SHALL:** Every returned external output shall remain non-authoritative candidate input until the owning component validates and accepts it.
- **REQ-SYS-EXTAI-008 — SHALL NOT:** An external integration shall not write directly to authoritative state, authorize privilege, activate a release, decide policy, or publish content.
- **REQ-SYS-EXTAI-009 — SHALL:** Controlled import shall preserve the owning component's schema, validation, authorization, provenance, and acceptance rules.
- **REQ-SYS-EXTAI-010 — SHALL:** External outputs used in authoritative or published work shall carry provenance sufficient to identify the integration, operation, actor or session, owning component, and accepted output.
- **REQ-SYS-EXTAI-011 — SHALL NOT:** Suno or Gamma shall not be invoked automatically by ingestion, indexing, classification, tagging, routing, synchronization, or background enrichment.
- **REQ-SYS-EXTAI-012 — SHALL:** Suno and Gamma workflows shall use controlled export, external processing, controlled re-import, provenance, user approval, and optional publication.
- **REQ-SYS-EXTAI-013 — SHALL:** Ariane external voice output shall be treated as a candidate navigation intent and shall pass local deterministic command validation before execution.
- **REQ-SYS-EXTAI-014 — SHALL:** Ambiguous or unrecognized Ariane voice intent shall be rejected or shall require explicit user confirmation before any side effect.
- **REQ-SYS-EXTAI-015 — SHALL:** Loss or removal of the Ariane voice adapter shall leave local keyboard, pointer, touch, menu, shortcut, accessibility, and deterministic-command navigation operational.
- **REQ-SYS-EXTAI-016 — SHALL:** Loss or removal of ChatGPT, Suno, or Gamma shall affect only the requested external capability and shall not disable unrelated local authority.
- **REQ-SYS-EXTAI-017 — SHALL NOT:** The system shall not silently substitute another provider, local model, or native AI capability when an approved external surface is unavailable.
- **REQ-SYS-EXTAI-018 — SHALL:** External operations shall fail without authoritative mutation when transfer, provider processing, validation, import, or acceptance fails.
- **REQ-SYS-EXTAI-019 — SHALL:** Removal of any external AI surface shall preserve the validity and provenance obligations of outputs previously accepted by owning components.
- **REQ-SYS-EXTAI-020 — SHALL:** Every conformance claim for an external AI surface shall be supported by registered tests and valid evidence covering activation, transfer, authority boundaries, provenance, failure, offline behavior, and removal.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Enablement

1. Resolve the active primary profile and overlays.
2. Confirm that the profile permits the integration.
3. Confirm that the integration is active in `contracts/integration-types.contract.json`.
4. Confirm that the requested capability is inside the registered capability scope.
5. Present the provider, capability, data-transfer, authority, provenance, and failure information to the user.
6. Keep the integration disabled until the user initiates a specific operation.
7. Reject unregistered providers, capabilities, or automatic triggers.

Profile permission does not imply continuous activation.

### 6.2 Generic external operation

1. The user selects the approved surface and capability.
2. The system identifies the owning component.
3. The user selects or enters the outbound content.
4. The interface discloses the data transfer.
5. The adapter exports only the admitted payload.
6. The provider performs external processing.
7. The adapter receives the output as candidate material.
8. The owning component validates the output.
9. Required provenance is recorded.
10. Required user or policy acceptance is obtained.
11. The owning component imports or rejects the candidate.
12. Publication, activation, or privilege remains a separate operation.

Cancellation or failure before acceptance produces no authoritative mutation.

### 6.3 ChatGPT candidate-content workflow

1. The user initiates a ChatGPT assistance operation.
2. The user supplies or selects the prompt and context.
3. The system discloses the outbound content.
4. ChatGPT returns candidate text, structure, analysis, or assistance.
5. The local workflow validates the returned format and scope.
6. The user reviews and accepts, edits, or rejects the candidate.
7. The owning component records accepted content and provenance when applicable.
8. Any authoritative change follows the owning component's normal workflow.

### 6.4 Suno or Gamma artifact workflow

1. The user explicitly selects content for export.
2. The system records the owning component and source references.
3. The system discloses the outbound data.
4. The adapter exports the admitted prompt or source material.
5. The provider returns a candidate artifact.
6. The adapter performs controlled re-import.
7. The owning component validates file type, schema, integrity, rights, scope, and policy.
8. A provenance receipt is recorded.
9. The user approves or rejects the artifact.
10. Optional publication uses the Publication Gateway and applicable publication contracts.

### 6.5 Ariane external voice workflow

1. The user starts an explicit voice session.
2. The interface discloses the audio and admitted session context.
3. The adapter sends only the active voice-session data.
4. The adapter returns a candidate navigation intent.
5. Ariane maps the candidate to the deterministic profile-enabled command set.
6. Ariane rejects unknown or prohibited commands.
7. Ariane requests confirmation for ambiguous or consequential commands when required.
8. Ariane executes the locally validated command.
9. A receipt is produced for critical transitions.
10. The voice session ends without continuous background listening.

### 6.6 Removal or disablement

1. Disable new operations for the integration.
2. Stop active sessions safely.
3. Clear temporary provider-specific session data according to the integration contract.
4. Preserve authoritative local data.
5. Preserve provenance for previously accepted outputs.
6. Preserve local core capabilities.
7. Remove provider credentials, endpoints, and adapter configuration where applicable.
8. Validate that no automatic fallback or hidden dependency remains.

## 7. Failure States and Safe Degradation

| Failure state | Required behavior | Preserved capability | Prohibited behavior |
| --- | --- | --- | --- |
| Integration not registered | Reject invocation | All local capabilities | Ad hoc provider use |
| Profile does not permit integration | Reject enablement | Profile-conformant local operation | Scope broadening |
| User does not explicitly initiate | Do not invoke | Local workflow | Background external call |
| Transfer disclosure unavailable | Block transfer | Local data and workflow | Hidden data export |
| Provider unavailable | Fail the requested operation | Unrelated local authority | Silent provider substitution |
| Network unavailable | Mark remote surface unavailable | Declared offline envelope | Repeated hidden retries |
| Output format invalid | Reject import | Existing valid state | Schema guessing |
| Output content unauthorized | Reject import or require policy review | Existing valid state | Direct authoritative mutation |
| Provenance incomplete | Block authoritative use or publication | Candidate artifact may remain quarantined | Provenance omission |
| User rejects output | Discard or retain only as non-authoritative candidate according to policy | Existing authoritative state | Automatic acceptance |
| Suno or Gamma returns partial artifact | Reject or quarantine the candidate | Existing media or presentation state | Partial authoritative import |
| Ariane intent ambiguous | Reject or request explicit confirmation | Local navigation | Guessed execution |
| Ariane voice unavailable | Disable voice only | Keyboard, pointer, touch, menus, shortcuts, accessibility, local commands | Local-navigation shutdown |
| ChatGPT unavailable | Disable requested assistance | Local editing and authoritative workflows | Native AI substitution |
| Adapter removed | Remove provider capability | Previously accepted local outputs and provenance | Core-system failure |
| External output conflicts with local policy | Reject or route to governed review | Existing local authority | Provider precedence |
| Receipt or evidence missing | Block the affected conformance, publication, or critical-transition claim | Independently supported operation | Unsupported claim |

A failure in an external surface never grants broader authority than a successful operation would have granted.

## 8. Cross-Component Interactions

| Interaction | Initiator | External surface | Local owner | Authority boundary |
| --- | --- | --- | --- | --- |
| Candidate text assistance | User-facing component or user | ChatGPT | Requesting owning component | ChatGPT returns candidate content only |
| Candidate media generation | User through kOA Mediatheque or another approved workflow | Suno | kOA Mediatheque or another registered owning component | Suno does not decide ingestion, routing, tagging, or publication |
| Candidate presentation generation | User through an approved workflow | Gamma | Requesting owning component | Gamma does not activate, publish, or own the accepted artifact |
| Candidate voice intent | Ariane voice session | Ariane voice adapter | Ariane Runtime | Adapter cannot execute local commands |
| Controlled export | Owning component | Approved surface | Owning component | Export does not transfer ownership |
| Controlled re-import | Approved surface | Integration adapter | Owning component | Import remains subject to local validation |
| Provenance recording | Owning component or adapter | Evidence subsystem | Evidence owner | Provenance does not grant acceptance |
| Publication | Owning component | Publication Gateway | Source domain and Publication Gateway | Generation or import does not imply publication |
| Policy review | Owning component | Governance Policy Runtime | Policy authority | Provider output has no policy authority |
| Resource control | Integration adapter and workers | Resource Governor | Resource Governor | Resource scheduling does not decide acceptance |
| Audit | Owning component or gateway | Audit Broker | Audit Broker | Evidence disclosure remains selective |

Direct provider-to-database, provider-to-publication, provider-to-privilege, provider-to-release, and provider-to-policy paths are prohibited.

## 9. Decision Closure and Prohibited Assumptions

### Accepted decisions

| Decision ID | Closed question |
| --- | --- |
| `DEC-AI-001` | Native AI is excluded from the global baseline; only registered external surfaces are permitted. |
| `DEC-SENT-001` | SenTient is an isolated optional workbench rather than a native or external baseline AI authority. |
| `DEC-MEDIATHEQUE-001` | Native kOA Mediatheque processing is deterministic; Suno and Gamma are explicit user-triggered adapters. |
| `DEC-ARI-001` | Ariane local navigation is non-AI; external voice is optional and locally validated. |
| `DEC-PROFILE-001` | External-surface availability is profile-scoped and does not imply universal enablement. |
| `DEC-DATA-001` | External services and adapters cannot write directly to component authoritative stores. |

### Prohibited assumptions

- A provider is permitted because it is technically reachable.
- A profile permits every integration by default.
- A user account connection authorizes continuous background access.
- Prompt context may include repositories, stores, secrets, or tenant data implicitly.
- Provider output is authoritative because it is fluent, structured, or requested by a user.
- ChatGPT output is an owner decision.
- Suno or Gamma may be triggered by ingestion or indexing.
- Generation approval implies publication approval.
- Ariane voice intent may bypass local deterministic validation.
- Voice unavailability disables local navigation.
- An unavailable provider may be replaced silently by another provider or local model.
- A removed integration invalidates accepted local outputs automatically.
- Provenance alone grants acceptance.
- User acceptance alone overrides component schema, policy, rights, or publication controls.
- SenTient belongs to the external integration allowlist.
- External AI is required for offline or core operation.
- A retry queue may be hidden, unbounded, or non-idempotent.
- External processing may acquire component, policy, privilege, release, or publication authority.

## 10. Validation Criteria

1. The metadata block parses as JSON and declares `DOC-SYS-010`, `active`, `en`, system layer, and global scope.
2. All eleven required sections exist in numerical order.
3. The approved-surface table contains exactly `chatgpt`, `suno`, `gamma`, and `ariane_voice_adapter`.
4. Every table classification, authority class, capability scope, and unavailable behavior matches `contracts/integration-types.contract.json`.
5. Every decision ID is accepted in `generated/decision-index.json`.
6. Every requirement ID appears exactly once in `generated/requirements-index.json`.
7. Every lock ID resolves to an active lock.
8. `TEST-SYS-EXTAI-001` verifies rejection of an unregistered provider.
9. `TEST-SYS-EXTAI-002` verifies explicit user initiation and absence of background activation.
10. `TEST-SYS-EXTAI-003` verifies transfer disclosure and outbound-data minimization.
11. `TEST-SYS-EXTAI-004` verifies absence of implicit repository, store, secret, tenant, or host access.
12. `TEST-SYS-EXTAI-005` verifies candidate-output status and controlled component acceptance.
13. `TEST-SYS-EXTAI-006` verifies that external services cannot write authoritative state, authorize privilege, activate releases, decide policy, or publish.
14. `TEST-SYS-EXTAI-007` verifies required provenance for accepted authoritative or published use.
15. `TEST-SYS-EXTAI-008` verifies that Suno and Gamma cannot be triggered by ingestion, indexing, classification, tagging, routing, synchronization, or background enrichment.
16. `TEST-SYS-EXTAI-009` verifies the controlled Suno and Gamma export, re-import, provenance, approval, and publication sequence.
17. `TEST-SYS-EXTAI-010` verifies Ariane candidate-intent handling and local deterministic command validation.
18. `TEST-SYS-EXTAI-011` verifies ambiguous and unrecognized Ariane intent rejection.
19. `TEST-SYS-EXTAI-012` verifies that loss of external voice preserves local Ariane navigation.
20. `TEST-SYS-EXTAI-013` verifies capability-scoped failure for ChatGPT, Suno, and Gamma.
21. `TEST-SYS-EXTAI-014` verifies absence of silent provider or local-model substitution.
22. `TEST-SYS-EXTAI-015` verifies disablement and removal without core failure.
23. `TEST-SYS-EXTAI-016` verifies preservation of provenance obligations for previously accepted outputs.
24. `TEST-SYS-EXTAI-017` verifies profile-scoped integration availability.
25. `TEST-SYS-EXTAI-018` verifies traceability to decisions, requirements, locks, tests, evidence, profiles, and owning components.
26. Active prose is English and contains no unresolved marker, placeholder, or template token.
27. The generated requirement projection matches the canonical requirement registry.

These criteria define required validation. They do not claim that implementation conformance or operational evidence already exists.

## 11. Non-Normative Examples

> **Non-normative example:** A user selects a paragraph and asks ChatGPT for a candidate rewrite. The interface shows the selected paragraph will be transferred. The returned text appears in a review surface. Nothing is written to the authoritative component until the user accepts it and the owning component validates the change.

> **Non-normative example:** A user selects media references and requests a Suno generation. The export contains only the selected prompt and inputs. The returned audio is quarantined as a candidate artifact, scanned and validated, assigned provenance, reviewed by the user, and admitted to kOA Mediatheque only after approval.

> **Non-normative example:** Gamma returns a presentation draft. The draft is imported into a component workspace and may be edited locally. Publication remains a separate request through the Publication Gateway.

> **Non-normative example:** The Ariane voice adapter returns an intent resembling a privileged operation. Ariane cannot execute it directly. The local command validator rejects it or routes it through the applicable policy and privilege workflow.

> **Non-normative example:** Internet connectivity disappears during a voice session. Voice becomes unavailable, but keyboard, pointer, touch, menu, shortcut, accessibility, and deterministic local commands continue.

> **Non-normative example:** ChatGPT is disabled from a profile. Existing locally accepted text remains part of the owning component's state with its existing provenance. No local editing, navigation, storage, kOA Mediatheque, language runtime, or resource-governance capability fails.
