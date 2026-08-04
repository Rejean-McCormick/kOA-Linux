<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "ADR-021",
  "document_class": "architecture_decision_record",
  "status": "active",
  "adr_status": "accepted",
  "language": "en",
  "layer": "architecture_decisions",
  "scope": [
    "global",
    "user_interface",
    "integration"
  ],
  "decision_date": "2026-08-03",
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json#/ai_model",
    "contracts/system.contract.json#/capability_model",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/integration-types.contract.json",
    "contracts/artifact-classes.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/exception-index.json"
  ],
  "decision_ids": [
    "DEC-ARIANE-001",
    "DEC-SYS-AI-001",
    "DEC-SYS-CAP-001",
    "DEC-SYS-COMP-001",
    "DEC-SYS-OFFLINE-001",
    "DEC-INT-001",
    "DEC-DATA-DISCLOSURE-001"
  ],
  "requirement_ids": [
    "REQ-ARIANE-001",
    "REQ-ARIANE-002",
    "REQ-ARIANE-003",
    "REQ-ARIANE-004",
    "REQ-ARIANE-005",
    "REQ-ARIANE-006",
    "REQ-ARIANE-007",
    "REQ-ARIANE-008",
    "REQ-ARIANE-009",
    "REQ-ARIANE-010",
    "REQ-ARIANE-011",
    "REQ-ARIANE-012",
    "REQ-ARIANE-013",
    "REQ-ARIANE-014",
    "REQ-ARIANE-015",
    "REQ-ARIANE-016",
    "REQ-ARIANE-017",
    "REQ-ARIANE-018",
    "REQ-ARIANE-019",
    "REQ-ARIANE-020",
    "REQ-ARIANE-021",
    "REQ-ARIANE-022",
    "REQ-ARIANE-023",
    "REQ-ARIANE-024",
    "REQ-ARIANE-025",
    "REQ-ARIANE-026",
    "REQ-ARIANE-027",
    "REQ-ARIANE-028",
    "REQ-ARIANE-029",
    "REQ-ARIANE-030",
    "REQ-ARIANE-031",
    "REQ-ARIANE-032",
    "REQ-ARIANE-033",
    "REQ-ARIANE-034",
    "REQ-ARIANE-035",
    "REQ-ARIANE-036",
    "REQ-ARIANE-037",
    "REQ-ARIANE-038",
    "REQ-ARIANE-039",
    "REQ-ARIANE-040"
  ],
  "lock_ids": [
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-GATE-001",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-OPS-001",
    "LOCK-OPS-002",
    "LOCK-OPS-003",
    "LOCK-OPS-004",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-GOV-001",
    "DOC-GOV-002",
    "DOC-GOV-003",
    "DOC-GOV-004",
    "DOC-GOV-005",
    "DOC-GOV-006",
    "DOC-GOV-007",
    "DOC-GOV-008",
    "DOC-CONST-002",
    "DOC-CONST-003",
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-007",
    "DOC-CONST-008",
    "DOC-CONST-009",
    "DOC-CONST-010",
    "DOC-SYS-000",
    "DOC-SYS-003",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-006",
    "DOC-SYS-008",
    "DOC-SYS-009",
    "DOC-SYS-010",
    "DOC-SYS-011",
    "DOC-SYS-012",
    "DOC-SYS-014",
    "DOC-SYS-015",
    "DOC-SYS-016",
    "DOC-SYS-017",
    "DOC-SYS-018",
    "DOC-SYS-019",
    "DOC-PROFILE-001",
    "DOC-PROFILE-002",
    "DOC-COMP-000",
    "DOC-COMP-001",
    "DOC-SEC-016",
    "DOC-OPS-003",
    "DOC-OPS-013",
    "DOC-CONF-003",
    "DOC-CONF-013",
    "DOC-CONF-019"
  ],
  "supersedes": [],
  "superseded_by": [],
  "tags": [
    "adr",
    "ariane",
    "local-navigation",
    "deterministic-ui",
    "optional-voice",
    "external-ai",
    "offline",
    "accessibility",
    "privacy",
    "controlled-export",
    "accepted-decision"
  ]
}
KOA:DOC-META:END -->

# ADR-021: Ariane Local Navigation with Optional External Voice

## 1. Status

**Accepted**

Decision date: **2026-08-03**

This ADR records the accepted architectural decision that Ariane provides deterministic local navigation without AI and can optionally use one approved external voice adapter.

The local navigation capability is always the authoritative interaction baseline.

External voice is an optional input and output convenience. It does not own navigation state, user authority, command meaning, policy, data, publication, privilege, recovery, or conformance.

The machine-readable system, component, profile, integration, requirement, and lock registries own the active facts. This ADR records the rationale, consequences, and rejected alternatives.

## 2. Context

Ariane is the local navigation surface for kOA.

Users need reliable access to:

- application discovery;
- route and menu navigation;
- status;
- settings;
- accessibility controls;
- local help;
- recovery entry points;
- governed workflows.

These capabilities need to work:

- without Internet access;
- during provider outages;
- on sovereign and offline nodes;
- when voice is disabled;
- when no microphone is present;
- when no model artifact is installed;
- when external credentials are absent;
- under resource pressure;
- during recovery.

Voice can improve accessibility and convenience, but voice processing can introduce:

- external data disclosure;
- ambiguous intent;
- provider dependency;
- model variability;
- latency;
- cost;
- microphone privacy risk;
- transcript retention;
- false confidence;
- command injection;
- accidental consequential action.

Making external voice part of the navigation authority would weaken offline continuity and blur the boundary between interpretation and action.

The architecture therefore separates deterministic local navigation from optional voice assistance.

## 3. Decision

Ariane uses the following model:

```text
deterministic_local_navigation
+ optional_external_voice_input
+ optional_external_voice_output
+ mandatory_local_validation
+ accessible_non_voice_fallback
```

The local engine owns:

- route identities;
- command identities;
- labels;
- menus;
- local state;
- command matching;
- ambiguity handling;
- confirmation;
- local action dispatch.

The optional external voice adapter can provide:

- candidate transcription;
- candidate intent;
- candidate pronunciation or synthesis;
- language or voice rendering assistance.

Returned material remains candidate data.

The local engine maps the candidate to registered local commands and parameters.

A consequential action still passes through the ordinary identity, authorization, confirmation, expected-state, receipt, and recovery path.

The approved external surface is:

```text
approved_ariane_voice_adapter
```

Other approved external AI surfaces in kOA do not automatically become Ariane voice integrations.

## 4. Local Navigation Architecture

### 4.1 Deterministic command model

Ariane local navigation uses registered records such as:

```text
command_id
route_id
label_id
language
synonyms
allowed_parameters
required_capability
required_identity
confirmation_class
failure_behavior
offline_behavior
```

Matching is deterministic and versioned.

The same accepted local input under the same command table and state produces the same navigation interpretation.

### 4.2 Local authority

Ariane is authoritative only for its local interaction state, including:

- current route;
- focused item;
- selected local command;
- visible or accessible choices;
- pending confirmation;
- navigation history where policy permits;
- adapter availability state.

It is not authoritative for the target component's business state.

### 4.3 Action dispatch

A local command dispatches through the owning interface.

Examples include:

- open an application route;
- show a status view;
- request a component action;
- open a settings panel;
- start a governed workflow;
- show a recovery option.

The target component validates and owns its resulting state.

### 4.4 Ambiguity

Ambiguity handling uses:

- bounded choices;
- clarification;
- no-op;
- safe cancellation;
- explicit target selection;
- explicit parameter selection.

Ariane does not guess a privileged or irreversible target.

### 4.5 Consequential actions

Consequential actions include:

- publication;
- disclosure;
- deletion;
- key or trust change;
- Release Set activation;
- privileged host change;
- payment or external commitment;
- account or identity change;
- recovery;
- protected evidence access.

Ariane can navigate to these workflows.

It cannot bypass their authority or confirmation.

### 4.6 Offline behavior

The local navigation engine and its registered command tables remain locally available according to the active profile.

External voice unavailability changes only the voice feature state.

It does not change the local route or command authority.

## 5. External Voice Boundary

### 5.1 Optional adapter

The external voice adapter is:

```text
optional
disabled_by_default
profile_scoped
explicitly_triggered
destination_bound
non_authoritative
removable
```

A profile can enable it for accessibility or convenience.

### 5.2 Capture

Capture begins only after an explicit user action or an explicitly configured accessibility trigger.

Ariane indicates:

- microphone activation;
- capture state;
- external transmission state;
- processing state;
- playback state;
- cancellation;
- failure.

Ambient continuous recording is outside the accepted baseline.

### 5.3 Export

An export contains only the selected minimum audio or text and the minimum context required to interpret it.

The export record identifies:

```text
request_id
purpose
requesting_identity_ref
profile_ref
selected_input
language
destination_ref
integration_ref
classification
retention
expiry
cost_boundary
provenance_ref
```

Secret values and unrestricted protected content remain excluded.

### 5.4 Reimport

Returned data can include:

```text
candidate_transcript
candidate_intent
candidate_parameters
candidate_speech
provider_metadata
```

The adapter cannot dispatch a local action directly.

Ariane receives the candidate and performs local validation.

### 5.5 Local validation

Local validation checks:

- adapter identity and version;
- response schema;
- request and response binding;
- candidate language;
- command identity;
- parameter allowlist;
- ambiguity;
- target state;
- confirmation class;
- timeout;
- replay or duplicate risk.

Unknown or unsafe candidates are rejected.

### 5.6 External synthesis

External synthesis can render text selected by Ariane.

The selected text remains locally owned.

Synthesis output does not change the meaning, authority, or result of the underlying local state.

### 5.7 Provider evidence

Provider acknowledgement proves only that the provider accepted or returned a request.

It does not prove:

- correct transcription;
- safe intent;
- authorized action;
- local acceptance;
- target completion;
- user confirmation.

## 6. Accessibility, Privacy, and Security

### 6.1 Equivalent non-voice access

Every voice-reachable capability has a non-voice path using applicable:

- keyboard;
- pointer;
- touch;
- switch access;
- local text input;
- screen reader;
- local menu;
- local command palette.

Profile contracts own the supported mechanisms.

### 6.2 Consent and control

Users can:

- enable or disable voice;
- select devices;
- cancel capture;
- cancel transmission where possible;
- inspect adapter state;
- inspect retention policy;
- remove credentials;
- remove the integration.

Ariane preserves the local fallback.

### 6.3 Microphone boundary

Microphone access is:

- profile-scoped;
- device-specific;
- revocable;
- time-bounded;
- visibly or audibly indicated;
- unavailable to the external provider except through the selected export.

The provider does not receive a direct local device handle.

### 6.4 Protected data

Voice requests apply:

- minimum necessary selection;
- privacy;
- consent;
- cultural rights;
- security classification;
- legal restrictions;
- audience;
- purpose;
- retention;
- recourse.

A voice convenience does not create broader disclosure authority.

### 6.5 Secrets

Ariane uses managed secret references for integration credentials.

It does not place secret values in:

- prompts;
- transcripts;
- logs;
- metrics;
- traces;
- receipts;
- accessible UI text;
- adapter configuration exports.

### 6.6 Prompt and command injection

Audio, transcript, provider output, external content, and spoken quoted text remain untrusted input.

They cannot redefine:

- authority order;
- command registration;
- identity;
- permissions;
- confirmation rules;
- target ownership;
- profile scope;
- local validation.

### 6.7 Receipt separation

A voice interaction can produce:

- provider interaction receipt;
- local interpretation receipt;
- consequential action receipt.

These records remain distinct.

The action receipt is owned by the target workflow.

## 7. Lifecycle and Failure Model

### 7.1 Enablement

Enablement verifies:

- compatible profile;
- approved adapter;
- endpoint registration;
- authentication;
- user or administrator configuration;
- privacy and retention;
- allowed languages;
- devices;
- cost and rate limits;
- local fallback;
- tests and evidence.

### 7.2 Request states

An external voice request can use:

```text
created
capturing
captured
export_pending
submitted
response_received
locally_validating
accepted
rejected
cancelled
failed
expired
```

Local action state remains separate.

### 7.3 Failure behavior

| Failure | Required behavior |
| --- | --- |
| No network | Continue local navigation and report voice unavailable. |
| Adapter disabled | Continue local navigation. |
| Credential invalid | Disable external submission and preserve local navigation. |
| Microphone unavailable | Offer non-voice input. |
| Capture permission denied | Offer non-voice input. |
| Provider timeout | Cancel or retry within bounds; no local action. |
| Response malformed | Reject. |
| Candidate command unknown | Reject or clarify. |
| Candidate ambiguous | Present bounded choices. |
| Candidate requests prohibited action | Reject. |
| Local validation unavailable | Reject candidate action. |
| Target component unavailable | Report target failure without changing local authority. |
| Action outcome unknown | Use the target workflow's reconciliation path. |
| Playback unavailable | Present accessible local text or another supported output. |
| Adapter state corrupt | Disable or reinstall the adapter without affecting navigation. |
| Integration removed | Revoke credentials and continue locally. |

### 7.4 Retry and duplicate safety

Voice submission retries are bounded.

A repeated accepted command uses the target workflow's idempotency model when duplicate effects are possible.

A repeated transcript is not itself authority for repeated execution.

### 7.5 Offline profiles

Offline-capable profiles preserve:

- local command tables;
- local labels;
- local navigation state;
- local accessible feedback;
- local confirmation;
- non-voice input;
- integration-disabled behavior.

External voice is unavailable unless the profile explicitly supports a registered reachable endpoint.

### 7.6 Removal

Removal:

1. disables the adapter;
2. stops active capture and requests;
3. revokes credentials;
4. removes endpoint configuration;
5. clears or retires adapter-local mutable state;
6. preserves required receipts and provenance;
7. verifies local navigation;
8. records the removal result.

## 8. Consequences

### 8.1 Positive consequences

The decision provides:

- reliable offline navigation;
- no mandatory AI dependency;
- accessible optional voice;
- explicit privacy boundaries;
- deterministic local command meaning;
- safe ambiguity handling;
- controlled external disclosure;
- provider removability;
- consistent consequential-action controls;
- separate provider and local receipts;
- resilience during provider failure.

### 8.2 Costs

The decision requires:

- local command registries;
- deterministic matching;
- accessible non-voice paths;
- explicit adapter integration;
- local validation;
- duplicate-safe action handling;
- profile configuration;
- device and credential management;
- retention and provenance records;
- voice-specific tests.

These costs preserve local sovereignty and safety.

### 8.3 User experience implications

Voice can make navigation faster, but a user can always continue without it.

When interpretation is ambiguous, Ariane asks for clarification rather than pretending certainty.

### 8.4 Operational implications

Operators monitor local navigation and external voice separately.

An external voice outage does not become a core navigation outage.

### 8.5 Security implications

The external adapter has no direct host, database, privileged-broker, or component-store access.

The strongest security property is that removing the adapter leaves the complete local navigation baseline operational.

## 9. Alternatives Considered

### 9.1 External voice as the primary navigation engine

**Rejected.**

This would make local access dependent on network, provider, credentials, model behavior, and disclosure.

### 9.2 Mandatory bundled local AI voice model

**Rejected.**

A mandatory model would weaken the native non-AI baseline, increase resource needs, and complicate lightweight and recovery profiles.

### 9.3 Free-form provider action dispatch

**Rejected.**

Allowing a provider to dispatch actions would bypass local command registration, ambiguity control, authorization, and target ownership.

### 9.4 Continuous ambient listening

**Rejected.**

Continuous capture creates excessive privacy, consent, storage, and accidental-trigger risk.

### 9.5 Voice-only accessibility path

**Rejected.**

Voice can fail or be unsuitable. Essential functions need equivalent non-voice access.

### 9.6 Multiple unregistered voice providers

**Rejected.**

Unbounded providers weaken destination control, data minimization, validation, cost control, and removability.

### 9.7 Voice integrated directly into every component

**Rejected.**

This would duplicate provider logic, weaken consistent privacy controls, and blur component boundaries.

### 9.8 No voice support

**Rejected.**

A controlled optional adapter improves accessibility and convenience without compromising the local baseline.

## 10. Conformance and Reconsideration

### 10.1 Conformance conditions

This decision is correctly implemented when:

1. Ariane local navigation works without AI or network;
2. command and route matching are deterministic;
3. ambiguous input cannot dispatch a consequential action;
4. voice is optional and profile-scoped;
5. only the approved Ariane voice adapter is enabled;
6. capture is explicit and indicated;
7. ambient continuous recording is absent;
8. exports use minimum necessary data;
9. protected and secret data controls pass;
10. returned data remains candidate-only;
11. local validation maps only to registered actions;
12. provider confidence does not establish local acceptance;
13. consequential workflows retain their ordinary controls;
14. every voice-reachable essential function has non-voice access;
15. microphone and output devices are bounded and revocable;
16. provider and action receipts remain separate;
17. retries, timeouts, cancellation, and duplicate safety are bounded;
18. local navigation continues through adapter failure or removal;
19. offline profiles retain full local navigation;
20. removal revokes credentials and preserves local state;
21. all profiles, integrations, commands, components, tests, evidence, receipts, and exceptions resolve;
22. no prohibited open-state marker enters active authority.

The principal validation entry point is:

```bash
uv run python docs/tools/validate_docs.py
```

Supporting checks include:

```text
docs/tools/check_ai_boundary.py
docs/tools/check_component_boundaries.py
docs/tools/check_profile_inheritance.py
docs/tools/check_integration_contracts.py
docs/tools/check_interfile_locks.py
docs/tools/check_traceability.py
docs/tools/check_decision_closure.py
docs/tools/check_no_unresolved_state.py
```

### 10.2 Reconsideration triggers

This ADR can be reconsidered when:

- a future accepted architecture defines a native non-AI local speech engine with different resource and privacy properties;
- an accessibility requirement cannot be met through the current adapter boundary;
- local deterministic command matching cannot support the required language or interaction model;
- a new external voice surface receives an accepted integration decision;
- provider-independent voice portability requires a different adapter abstraction;
- offline profiles require a separately governed local voice artifact class;
- evidence shows that local validation cannot safely contain provider ambiguity.

Reconsideration requires a new accepted ADR and canonical registry changes.

Existing interactions and receipts remain historically interpretable under this ADR.

## 11. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-ARIANE-001,REQ-ARIANE-002,REQ-ARIANE-003,REQ-ARIANE-004,REQ-ARIANE-005,REQ-ARIANE-006,REQ-ARIANE-007,REQ-ARIANE-008,REQ-ARIANE-009,REQ-ARIANE-010,REQ-ARIANE-011,REQ-ARIANE-012,REQ-ARIANE-013,REQ-ARIANE-014,REQ-ARIANE-015,REQ-ARIANE-016,REQ-ARIANE-017,REQ-ARIANE-018,REQ-ARIANE-019,REQ-ARIANE-020,REQ-ARIANE-021,REQ-ARIANE-022,REQ-ARIANE-023,REQ-ARIANE-024,REQ-ARIANE-025,REQ-ARIANE-026,REQ-ARIANE-027,REQ-ARIANE-028,REQ-ARIANE-029,REQ-ARIANE-030,REQ-ARIANE-031,REQ-ARIANE-032,REQ-ARIANE-033,REQ-ARIANE-034,REQ-ARIANE-035,REQ-ARIANE-036,REQ-ARIANE-037,REQ-ARIANE-038,REQ-ARIANE-039,REQ-ARIANE-040 -->
- **REQ-ARIANE-001 — SHALL:** Ariane provide complete local navigation through deterministic non-AI behavior independent of every external voice, speech, model, or network service.
- **REQ-ARIANE-002 — SHALL:** Ariane local navigation remain available during network loss, provider outage, voice-adapter failure, credential expiry, integration removal, and external AI unavailability.
- **REQ-ARIANE-003 — SHALL NOT:** External voice availability be required for local startup, menu discovery, application launch, settings access, recovery access, status inspection, or ordinary navigation.
- **REQ-ARIANE-004 — SHALL:** The local navigation engine use registered commands, routes, states, labels, permissions, and deterministic matching rules.
- **REQ-ARIANE-005 — SHALL NOT:** A model inference, free-form external interpretation, or provider response directly determine a local navigation transition.
- **REQ-ARIANE-006 — SHALL:** Every local navigation action resolve to one registered capability, route, command, or explicitly bounded local interaction.
- **REQ-ARIANE-007 — SHALL:** Ambiguous local input produce clarification, bounded choices, or no action rather than an inferred privileged or consequential action.
- **REQ-ARIANE-008 — SHALL NOT:** Ariane execute privileged, publication, disclosure, governance, release, identity, security, recovery, or data-mutation actions solely from a voice interpretation.
- **REQ-ARIANE-009 — SHALL:** Consequential actions reached through Ariane use the same identity, authorization, confirmation, expected-state, receipt, and recovery controls as the equivalent non-voice workflow.
- **REQ-ARIANE-010 — SHALL:** Ariane preserve visible or otherwise accessible confirmation of the interpreted command, target, scope, and expected effect before a consequential action.
- **REQ-ARIANE-011 — SHALL:** External voice be optional, disabled by default unless the active profile explicitly enables the approved Ariane voice adapter.
- **REQ-ARIANE-012 — SHALL:** The approved Ariane voice adapter be the only external voice integration permitted by the active baseline.
- **REQ-ARIANE-013 — SHALL NOT:** An unregistered speech, voice, transcription, synthesis, model, assistant, or provider endpoint be used by Ariane.
- **REQ-ARIANE-014 — SHALL:** Every external voice request use an explicit user trigger or explicitly configured accessibility trigger with visible or audible state.
- **REQ-ARIANE-015 — SHALL NOT:** Ariane record, stream, transcribe, synthesize, or export ambient audio continuously by default.
- **REQ-ARIANE-016 — SHALL:** Every external voice export declare purpose, selected audio or text, destination, integration, classification, retention, expiry, provenance, cost boundary, and local acceptance behavior.
- **REQ-ARIANE-017 — SHALL:** External voice input be reduced to the minimum segment and context necessary for the declared interaction.
- **REQ-ARIANE-018 — SHALL NOT:** Ariane export unrelated screen content, private proof, unrestricted logs, credentials, secret values, raw private keys, protected personal data, or cultural-restricted content with a voice request.
- **REQ-ARIANE-019 — SHALL:** Returned transcription, intent, synthesis, or other provider output remain non-authoritative candidate data until local validation.
- **REQ-ARIANE-020 — SHALL:** Local validation map a returned candidate only to registered commands, routes, labels, languages, and bounded parameters.
- **REQ-ARIANE-021 — SHALL NOT:** Provider confidence, model confidence, transcript confidence, natural-language fluency, or provider acknowledgement substitute for local command validation.
- **REQ-ARIANE-022 — SHALL:** A candidate that does not map uniquely and safely to a registered local action produce clarification or rejection.
- **REQ-ARIANE-023 — SHALL:** Ariane preserve provenance linking user trigger, selected input, adapter version, provider interaction, returned candidate, local mapping, confirmation, action, and result.
- **REQ-ARIANE-024 — SHALL:** Ariane keep provider interaction records separate from local authoritative action receipts.
- **REQ-ARIANE-025 — SHALL:** Voice-related logs, metrics, traces, receipts, and evidence exclude raw audio and transcript content unless a distinct retention policy explicitly authorizes the selected minimum data.
- **REQ-ARIANE-026 — SHALL:** The active profile define permitted languages, voice features, input and output devices, network behavior, accessibility behavior, retention, and offline fallback.
- **REQ-ARIANE-027 — SHALL:** Ariane expose an accessible non-voice path for every capability made reachable through external voice.
- **REQ-ARIANE-028 — SHALL NOT:** A voice-only interface become the exclusive path to consent, privacy, security, recovery, recourse, administration, or essential user functions.
- **REQ-ARIANE-029 — SHALL:** Ariane provide clear local indicators when microphone capture, external transmission, processing, playback, or failure is active.
- **REQ-ARIANE-030 — SHALL:** Microphone and audio-output device access use profile-scoped permissions, explicit device selection, bounded activation, and revocation.
- **REQ-ARIANE-031 — SHALL NOT:** The external voice adapter receive direct access to local databases, component stores, Audit Broker, privileged broker, secret store, or device-management interfaces.
- **REQ-ARIANE-032 — SHALL:** External voice integration use registered APIs and controlled export and reimport boundaries.
- **REQ-ARIANE-033 — SHALL:** Ariane rate-limit, size-limit, timeout, cancel, and bound retries for external voice interactions.
- **REQ-ARIANE-034 — SHALL:** Repeated voice requests use idempotency where a repeated accepted action could otherwise create duplicate effects.
- **REQ-ARIANE-035 — SHALL:** Provider failure, timeout, malformed output, incompatible adapter output, or unknown outcome preserve local state and report an explicit bounded failure.
- **REQ-ARIANE-036 — SHALL:** Ariane continue deterministic local navigation while external voice requests are deferred, cancelled, failed, or unavailable.
- **REQ-ARIANE-037 — SHALL:** Removal of the external voice adapter revoke its credentials, disable endpoints, clear or retire adapter-local mutable state, preserve required provenance and receipts, and leave Ariane local navigation intact.
- **REQ-ARIANE-038 — SHALL NOT:** Removal of external voice delete local navigation state, component-owned data, canonical authority, audit records, recourse state, or accepted user configuration outside the adapter scope.
- **REQ-ARIANE-039 — SHALL:** Every exception affecting Ariane voice be profile-scoped, time-bounded, data-minimized, non-authoritative, supported by compensating controls, tests, evidence, and explicit non-voice fallback.
- **REQ-ARIANE-040 — SHALL:** Ariane conformance include deterministic local navigation, default-optional voice, approved-adapter restriction, explicit capture, minimum export, local validation, accessible fallback, device and secret controls, bounded retries, offline continuity, removability, reference resolution, and absence of prohibited open-state markers.
<!-- GENERATED:REQUIREMENTS:END -->
