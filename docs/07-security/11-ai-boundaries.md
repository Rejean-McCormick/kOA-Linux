<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SEC-011",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "security",
  "scope": [
    "global",
    "security_boundary:ai",
    "integration_class:external_ai",
    "component:sentient",
    "capability:ariane_external_voice"
  ],
  "canonical_refs": [
    "07-security/00-threat-model.md",
    "01-constitution/04-explicit-authority.md",
    "02-system/01-system-context.md",
    "02-system/11-ariane-system-boundary.md",
    "02-system/19-release-and-artifact-identity.md",
    "03-profiles/11-high-assurance.md",
    "04-components/subsystems/semantik-architect.md",
    "04-components/publication-gateway.md",
    "06-lifecycle/08-kristal-artifacts.md",
    "06-lifecycle/18-sbom-provenance-and-signing.md",
    "contracts/system.contract.json",
    "generated/component-catalog.json",
    "contracts/integration-types.contract.json",
    "generated/profile-catalog.json",
    "contracts/profiles/high-assurance.profile.json",
    "contracts/subsystems/sentient.subsystem.json",
    "contracts/subsystems/ariane.subsystem.json",
    "contracts/components/koa-mediatheque.component.json",
    "contracts/integrations/uckk-publication.integration.json",
    "contracts/subsystems/semantik-architect.subsystem.json",
    "contracts/components/governance-policy-runtime.component.json",
    "contracts/components/identity-and-trust.component.json",
    "contracts/components/audit-broker.component.json",
    "contracts/components/resource-governor.component.json",
    "contracts/components/publication-gateway.component.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-AI-001",
    "DEC-SENT-001",
    "DEC-ARI-001",
    "DEC-MEDIATHEQUE-001",
    "DEC-UCKK-EXT-001",
    "DEC-LANG-001",
    "DEC-KRISTAL-001",
    "DEC-AUTH-001",
    "DEC-IDENT-001",
    "DEC-DATA-001",
    "DEC-COMP-001",
    "DEC-GOV-001",
    "DEC-PRIV-001",
    "DEC-LIFE-001"
  ],
  "requirement_ids": [
    "REQ-SEC-AI-001",
    "REQ-SEC-AI-002",
    "REQ-SEC-AI-003",
    "REQ-SEC-AI-004",
    "REQ-SEC-AI-005",
    "REQ-SEC-AI-006",
    "REQ-SEC-AI-007",
    "REQ-SEC-AI-008",
    "REQ-SEC-AI-009",
    "REQ-SEC-AI-010",
    "REQ-SEC-AI-011",
    "REQ-SEC-AI-012",
    "REQ-SEC-AI-013",
    "REQ-SEC-AI-014",
    "REQ-SEC-AI-015",
    "REQ-SEC-AI-016",
    "REQ-SEC-AI-017",
    "REQ-SEC-AI-018",
    "REQ-SEC-AI-019",
    "REQ-SEC-AI-020",
    "REQ-SEC-AI-021",
    "REQ-SEC-AI-022",
    "REQ-SEC-AI-023",
    "REQ-SEC-AI-024",
    "REQ-SEC-AI-025",
    "REQ-SEC-AI-026",
    "REQ-SEC-AI-027",
    "REQ-SEC-AI-028",
    "REQ-SEC-AI-029",
    "REQ-SEC-AI-030",
    "REQ-SEC-AI-031",
    "REQ-SEC-AI-032",
    "REQ-SEC-AI-033",
    "REQ-SEC-AI-034",
    "REQ-SEC-AI-035",
    "REQ-SEC-AI-036",
    "REQ-SEC-AI-037",
    "REQ-SEC-AI-038",
    "REQ-SEC-AI-039",
    "REQ-SEC-AI-040",
    "REQ-SEC-AI-041",
    "REQ-SEC-AI-042"
  ],
  "lock_ids": [
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-SENT-001",
    "LOCK-MEDIATHEQUE-001",
    "LOCK-MEDIATHEQUE-002",
    "LOCK-UCKK-EXT-001",
    "LOCK-ARI-001",
    "LOCK-ARI-002",
    "LOCK-DATA-001",
    "LOCK-COMP-001",
    "LOCK-AUTH-001",
    "LOCK-AUTH-002",
    "LOCK-GOV-001",
    "LOCK-PRIV-001",
    "LOCK-LIFE-001",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-UCKK-EXT-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-SEC-000",
    "DOC-CONST-004",
    "DOC-SYS-001",
    "DOC-SYS-011",
    "DOC-SYS-019",
    "DOC-PROF-011",
    "DOC-COMP-PUBGATE",
    "DOC-LIFE-008",
    "DOC-LIFE-018"
  ],
  "tags": [
    "ai-boundaries",
    "external-ai",
    "no-ai",
    "candidate-input",
    "data-transfer",
    "provenance",
    "sentient",
    "ariane-voice",
    "chatgpt",
    "suno",
    "gamma",
    "deterministic-core",
    "prompt-injection",
    "human-review"
  ]
}
KOA:DOC-META:END -->

# AI Boundaries

## 1. Purpose

This document defines the global kOA security boundary for artificial-intelligence capabilities, AI-capable external services, AI-assisted development, optional voice processing, and the SenTient workbench.

The governing principle is:

`text
AI can assist.
AI does not become invisible authority.
`

The boundary preserves:

- explicit user or accountable workflow initiation;
- data minimization and no-AI restrictions;
- candidate status;
- source and operation provenance;
- deterministic validation and authorization;
- human, expert, steward, community, legal, or publication review;
- component-owned admission;
- provider removability;
- offline core operation;
- credible recovery and exit.

The global baseline does not depend on a native AI model.

## 2. Scope

This document applies to:

- ChatGPT;
- Suno;
- Gamma;
- the approved Ariane voice adapter;
- SenTient;
- future local or remote AI-capable integrations;
- AI-assisted code, documentation, schema, migration, grammar, policy, media, presentation, query, and content candidates;
- prompts, context packages, retrieved content, attachments, tool requests, candidate outputs, review records, and provenance;
- online, offline, developer, build-farm, high-assurance, sovereign, and exit contexts.

It covers:

- capability registration;
- data eligibility;
- transfer preview and confirmation;
- prompt-injection resistance;
- tool boundaries;
- output quarantine and admission;
- review and evidence;
- failure, suspension, removal, incident response, withdrawal, and recovery.

It does not define:

- provider commercial terms;
- one model family;
- one prompt format;
- one transcription protocol;
- one media-generation workflow beyond registered integration contracts;
- one local-model runtime;
- native AI classification, routing, summarization, embedding, or autonomous-agent behavior.

## 3. Canonical References

| Canonical reference | Ownership |
| --- | --- |
| `contracts/system.contract.json#/ai_boundary` | Global native-AI exclusions, allowed external surfaces, common capability rules, and system-wide failure behavior. |
| `contracts/integration-types.contract.json` | Provider, endpoint, data-class, operation, retention, network, credential, output, and removal contracts. |
| `generated/component-catalog.json` | Component identities, data ownership, relationships, and global cross-component boundaries. |
| `contracts/components/sentient.component.json` | SenTient isolation, profiles, stores, interfaces, states, workflows, resources, candidate output, and evidence. |
| `contracts/components/ariane-runtime.component.json` | Local navigation, optional voice candidate, confirmation, authorization, execution, failure, and evidence. |
| `contracts/components/koa-mediatheque.component.json` | Deterministic local media ingestion, original preservation, metadata, rights, and controlled external-candidate admission. |
| `contracts/integrations/uckk-publication.integration.json` | Explicit authorized publication from kOA Mediatheque to the external UCKK Moodle platform. |
| `contracts/components/gf-wordbench.component.json` | Reviewed language-source admission and deterministic compilation. |
| `contracts/components/semantik-architect-runtime.component.json` | Deterministic language-pack verification, activation, and rendering. |
| `contracts/components/governance-policy-runtime.component.json` | Data-transfer, tool, publication, exception, consent, rights, and capability decisions. |
| `contracts/components/identity-and-trust.component.json` | User, workflow, integration, provider, model, credential, artifact, reviewer, and revocation identity. |
| `contracts/components/audit-broker.component.json` | Classified AI-operation, transfer, review, rejection, incident, and withdrawal evidence. |
| `contracts/components/resource-governor.component.json` | Task activation, quotas, concurrency, timeout, cancellation, queue, and idle-shutdown controls. |
| `07-security/00-threat-model.md` | Global assets, adversaries, trust boundaries, threat IDs, residual risk, and security-review process. |
| `02-system/11-ariane-system-boundary.md` | Deterministic navigation, voice candidate boundary, sensitive confirmation, and user control. |
| `04-components/gf-wordbench.md` | External candidate to reviewed source revision and deterministic language build. |
| `04-components/publication-gateway.md` | Reviewed private-to-public content disclosure after local admission. |
| `06-lifecycle/08-kristal-artifacts.md` | Candidate claim, review, recognition, Runtime Pack, query, and activation boundaries. |
| `06-lifecycle/18-sbom-provenance-and-signing.md` | AI contribution provenance in release-grade artifacts and supply-chain evidence. |
| `generated/test-catalog.json` | AI, security, component, profile, operations, lifecycle, exit, and documentation tests. |
| `generated/evidence-catalog.json` | Executed transfer, review, admission, rejection, removal, and conformance evidence. |

## 4. Model and Responsibilities

### 4.1 Baseline model

The native baseline contains no:

- generative model;
- classifier;
- summarizer;
- embedding model;
- autonomous routing model;
- autonomous agent;
- AI-generated category engine;
- AI-based ingestion decision;
- hidden AI ranking requirement;
- AI dependency for authorization, policy, activation, recovery, or offline operation.

Deterministic local functions remain distinct from AI even when they automate work.

Examples include:

- schema validation;
- rule evaluation;
- fixed search;
- checksums and artifact verification;
- deterministic text extraction;
- explicit user category assignment;
- grammar compilation;
- SemantiK rendering;
- Ariane local navigation;
- kOA Mediatheque ingestion and transcoding;
- bounded workflow routing based on declared rules.

### 4.2 Approved external surfaces

The canonical allowlist is owned by `contracts/system.contract.json`.

This document displays its accepted projection:

<!-- GENERATED:EXTERNAL-AI-SURFACES:BEGIN source=contracts/system.contract.json#/ai_boundary/allowed_external_surfaces -->
| Surface | Intended assistive role | Entry condition | Return role | Boundary |
| --- | --- | --- | --- | --- |
| ChatGPT | External user assistance for drafting, planning, analysis, or candidate content. | Entry condition | Explicit user action; manual use or registered integration. | Return role | Candidate text or structured artifact. | Boundary | No implicit system-data upload or authoritative write. |
| Suno | External candidate audio or music generation. | Entry condition | Explicit user selection and controlled export. | Return role | Candidate media artifact. | Boundary | No automatic kOA Mediatheque admission, UCKK publication, identity assignment, or rights decision. |
| Gamma | External candidate presentation or visual-content generation. | Entry condition | Explicit user selection and controlled export. | Return role | Candidate presentation or visual artifact. | Boundary | No automatic workflow, publication, or canonical-content admission. |
| Approved Ariane voice adapter | Optional speech capture and candidate transcript or intent generation. | Entry condition | Explicit voice-mode activation and scoped audio transfer. | Return role | Candidate transcript or structured command. | Boundary | Local Ariane performs deterministic resolution, confirmation, authorization, and execution. |
<!-- GENERATED:EXTERNAL-AI-SURFACES:END -->

A surface outside this list remains unavailable until the canonical registry and all dependent contracts are validly changed.

A named surface without a registered automated integration can be used only through a manual user-mediated process that does not silently transfer system data.

### 4.3 Capability classes

| Capability ID | Capability | Permitted candidate result | Admission owner |
| --- | --- | --- | --- |
| `AI-CAP-001` | Candidate drafting | Permitted candidate result | Required admission owner | Owning content workflow |
| `AI-CAP-002` | Candidate summarization | Permitted candidate result | Required admission owner | Owning content or evidence workflow |
| `AI-CAP-003` | Candidate translation | Permitted candidate result | Required admission owner | GF Wordbench or owning content workflow |
| `AI-CAP-004` | Candidate extraction | Permitted candidate result | Required admission owner | Owning component admission |
| `AI-CAP-005` | Candidate reconciliation | Permitted candidate result | Required admission owner | SenTient or owning review workflow |
| `AI-CAP-006` | Candidate media generation | Permitted candidate result | Required admission owner | kOA Mediatheque controlled admission and rights review |
| `AI-CAP-007` | Voice candidate | Permitted candidate result | Required admission owner | Ariane local deterministic resolution |
| `AI-CAP-008` | Development assistance | Permitted candidate result | Required admission owner | Repository owner review and validation |

These capabilities describe possible candidate roles. They do not authorize one provider, data class, tenant, profile, or use automatically.

### 4.4 Prohibited effects

| Prohibition ID | Category | Prohibited effect |
| --- | --- | --- |
| `AI-PROH-001` | Privilege or host control | Prohibited effect | Grant Linux privilege, invoke arbitrary root, alter boot, change firewall, mount storage, or handle protected keys. |
| `AI-PROH-002` | Authority fabrication | Prohibited effect | Create, infer, approve, or expand governance, delegation, exception, emergency, consent, or cultural authority. |
| `AI-PROH-003` | Direct authoritative mutation | Prohibited effect | Write component source tables, active policy, active release, active Runtime Pack, workflow state, or public state directly. |
| `AI-PROH-004` | Autonomous publication or activation | Prohibited effect | Publish content, sign artifacts, release channels, activate artifacts, roll back, revoke, or restore without the owning deterministic lifecycle. |
| `AI-PROH-005` | Hidden ranking or routing | Prohibited effect | Become the undisclosed baseline for civic value, task routing, moderation, category generation, or ingestion decisions. |
| `AI-PROH-006` | Rights determination | Prohibited effect | Determine final consent, attribution, audience, cultural authority, withdrawal, or export eligibility. |
| `AI-PROH-007` | Secret access | Prohibited effect | Read unrestricted secrets, signing material, recovery material, private credentials, or unrelated tenant data. |
| `AI-PROH-008` | Core dependency | Prohibited effect | Become the only path to local correctness, navigation, rendering, ingestion, query, policy, recovery, or exit. |

A provider's ability to perform an action does not grant kOA authority to request or accept it.

### 4.5 Data eligibility

| Data class or restriction | External AI eligibility | Handling principle |
| --- | --- | --- |
| `public` | External AI eligibility | Eligible only when source rights and destination policy permit. | Handling principle | Minimize and preview. |
| `internal` | External AI eligibility | Eligible only through an explicit approved integration and declared purpose. | Handling principle | Exclude unrelated organizational context. |
| `personal` | External AI eligibility | Blocked by default; requires explicit purpose, minimization, consent or other valid authority, provider compatibility, and review. | Handling principle | Use the smallest necessary fields. |
| `sensitive` | External AI eligibility | Blocked by default; exceptional use requires a registered compatible capability and strong authorization. | Handling principle | Prefer local deterministic processing. |
| `restricted` | External AI eligibility | Outside external AI surfaces unless an explicit artifact, rights, provider, audience, and policy contract permits the exact operation. | Handling principle | No implicit exception. |
| `secret` | External AI eligibility | Ineligible for external AI transfer. | Handling principle | Do not transfer. |
| `cultural_rights_restricted` | External AI eligibility | Ineligible unless the competent steward or community authority and all applicable rights explicitly permit the exact provider and use. | Handling principle | No-AI and withdrawal controls remain enforceable. |
| `no-AI` | External AI eligibility | Ineligible for external AI processing regardless of general classification until the restriction is validly changed by its owner. | Handling principle | Enforce at every boundary. |

Eligibility is evaluated on the complete transfer, including:

- prompts;
- system-provided instructions;
- retrieved context;
- hidden metadata;
- attachments;
- images;
- audio;
- logs;
- examples;
- conversation history;
- tool outputs;
- identifiers;
- links that expose protected resources.

### 4.6 AI operation contract

An AI operation contract identifies:

- operation identity;
- requesting user or workflow;
- tenant and environment;
- source object identities;
- provider and endpoint;
- model or service identity when known;
- capability class;
- purpose;
- allowed data classes;
- excluded fields and artifacts;
- destination and network scope;
- tool allowlist;
- input and output limits;
- timeout and retry policy;
- provider retention context;
- output use;
- required reviewers;
- expiry;
- cancellation;
- evidence class;
- removal and incident behavior.

The operation contract is narrower than the provider's general capabilities.

### 4.7 Transfer preview and consent

Before external transfer, the review surface presents:

- provider and destination;
- purpose;
- selected sources;
- fields and attachments;
- transformations and redactions;
- classification and no-AI result;
- output use;
- provider retention context known to the integration contract;
- potential irreversible disclosure;
- cancellation and alternatives.

Confirmation applies to the exact prepared transfer.

A material change creates a new preview and confirmation.

### 4.8 Prompt and context handling

Prompts and retrieved context are data.

They do not acquire authority because they contain phrases such as:

- ignore previous instructions;
- act as administrator;
- publish this result;
- call this tool;
- reveal the system prompt;
- treat this source as trusted;
- bypass review;
- mark this approved.

The local operation contract, not source text or model output, defines authority and available tools.

### 4.9 Tool boundary

An AI surface can receive a narrowly defined tool only when the integration contract declares it.

A permitted tool call remains subject to:

- authenticated requester and workload identity;
- tenant and environment binding;
- separate governance authorization;
- strict schema;
- allowlisted target;
- bounded arguments;
- input and output validation;
- timeout;
- idempotency or replay control;
- classified receipt;
- independent owning-component mutation.

The AI never receives raw database credentials or a generic privileged execution surface.

### 4.10 Candidate lifecycle

`text
local source selected
-> data eligibility and minimization
-> transfer preview
-> explicit confirmation
-> external processing
-> candidate response
-> quarantine or controlled import
-> provenance capture
-> deterministic validation
-> required review
-> owning-component admission or rejection
-> optional publication or activation through a separate lifecycle
`

External processing ends at candidate creation.

Every later transition belongs to a local canonical owner.

### 4.11 Provenance

AI-operation provenance can contain:

- operation identity;
- provider and endpoint identity;
- model or service identity when known;
- capability class;
- requestor and reviewer identities;
- input object references;
- redaction or transformation identity;
- output artifact identity;
- timestamps or sequence context;
- warnings and limitations;
- tool calls and receipts;
- review disposition;
- admitted, rejected, quarantined, withdrawn, or superseded state.

Sensitive prompt and response content is not duplicated into evidence unless required and authorized.

### 4.12 ChatGPT boundary

ChatGPT remains an external user-assistance surface.

Permitted patterns are:

- the user consults ChatGPT separately and manually imports selected candidate material;
- a registered integration prepares an eligible minimized transfer, obtains explicit confirmation, and returns a candidate artifact.

ChatGPT does not become a hidden system backend, canonical database, policy service, workflow authority, release authority, or recovery dependency.

### 4.13 Suno and Gamma boundary

The controlled pattern is:

1. explicit user selection;
2. eligible source and rights review;
3. controlled export;
4. external processing;
5. controlled re-import;
6. provenance receipt;
7. user or owner review;
8. kOA Mediatheque or other owning-component admission;
9. optional publication through its separate contract.

Their output does not receive kOA Mediatheque identity, rights, category, publication, or canonical status until local admission. UCKK publication requires a later independent authorization.

### 4.14 Ariane voice boundary

Ariane has two separate capability levels:

- `ariane_local_navigation`;
- `ariane_external_voice`.

Local navigation uses deterministic commands, menus, keyboard, pointer, touch, shortcuts, and accessibility controls.

External voice produces a candidate transcript or command.

Ariane locally:

- displays or otherwise exposes the candidate;
- resolves it against the active Atlas and driver;
- validates parameters;
- evaluates authority;
- requests action-specific confirmation;
- executes through the normal deterministic interface;
- records the result.

### 4.15 SenTient boundary

SenTient is a component workbench, not the global AI baseline.

It is:

- optional;
- isolated;
- task activated;
- available only in compatible developer and build profiles;
- absent from `user_lightweight`;
- non-authoritative;
- unable to write another component's stores;
- unable to control host privilege;
- unnecessary for core offline operation.

Its candidate outputs preserve source lineage, alternatives, contradictions, uncertainty, method identity, and reviewer disposition.

### 4.16 Future local models

A local model remains untrusted code and an optional capability.

Local execution does not eliminate:

- prompt injection;
- malicious model files;
- dependency compromise;
- secret exposure;
- rights restrictions;
- provenance requirements;
- resource exhaustion;
- model drift;
- hallucination;
- review;
- removal;
- rollback and incident response.

A future local-model design uses a new accepted contract rather than being inferred from this document.

### 4.17 AI-assisted development and documentation

AI-generated code, tests, configurations, schemas, migrations, grammar, policy, documentation, and release material remain candidate changes.

They follow:

- canonical owner resolution;
- accepted decision closure;
- source review;
- dependency and supply-chain review;
- deterministic validation;
- test execution;
- evidence;
- generated-file protection;
- profile scoping;
- identifier lifecycle;
- human accountability.

An AI agent does not convert prose into new architecture by assumption.

### 4.18 Threats and controls

| Threat ID | Threat | Scenario | Control themes |
| --- | --- | --- | --- |
| `AI-THREAT-001` | Prompt or indirect injection | Scenario | Source content attempts to override authority, request tools, reveal secrets, or alter the task. | Control themes | Treat content as data; fixed system capability; tool allowlist; output validation; no authority inheritance. |
| `AI-THREAT-002` | Sensitive-data exfiltration | Scenario | Selected or retrieved context includes protected data not needed for the task. | Control themes | Eligibility engine; minimization; preview; confirmation; destination controls; no-AI enforcement; receipts. |
| `AI-THREAT-003` | Hallucinated authority | Scenario | Output asserts approval, policy, identity, recognition, legal status, or cultural authority. | Control themes | Candidate labeling; source requirements; deterministic owner verification; human or steward review. |
| `AI-THREAT-004` | Tool or privilege abuse | Scenario | The model attempts commands, database writes, signing, publication, network expansion, or host operations. | Control themes | No unrestricted tools; schema-bound calls; separate authorization; kOA Node Agent isolation; receipts. |
| `AI-THREAT-005` | Provider or model drift | Scenario | Behavior, retention, endpoint, model, safety policy, or output format changes. | Control themes | Registered identities; compatibility monitoring; reapproval; pinned capability contract; disable on incompatible drift. |
| `AI-THREAT-006` | Provenance loss | Scenario | Output is copied into authoritative work without provider, source, task, or review context. | Control themes | Candidate artifact identity; provenance; import workflow; review disposition; traceability. |
| `AI-THREAT-007` | Overreliance and automation bias | Scenario | Reviewers accept fluent output without source or domain verification. | Control themes | Materiality-based review; independent checks; uncertainty display; reviewer accountability; sampled audits. |
| `AI-THREAT-008` | Rights and cultural extraction | Scenario | Protected content is processed or generated outside valid consent, audience, attribution, or steward authority. | Control themes | Rights policy; no-AI; explicit steward decision; controlled export; withdrawal and downstream remediation. |
| `AI-THREAT-009` | Generated-code compromise | Scenario | Candidate code or configuration introduces vulnerabilities, hidden dependencies, unsafe commands, or supply-chain changes. | Control themes | Code review; isolated tests; SBOM and provenance; dependency review; security tests; no protected credentials. |
| `AI-THREAT-010` | Cost or resource exhaustion | Scenario | Large requests, repeated generations, media jobs, or retries consume money, bandwidth, CPU, storage, or review capacity. | Control themes | Quotas; task activation; size limits; cancellation; bounded retries; resource and cost receipts. |
| `AI-THREAT-011` | Retention and secondary use | Scenario | Provider stores prompts or outputs longer or uses them for purposes incompatible with source rights. | Control themes | Provider contract; transfer decision; minimization; no-AI; retention disclosure; deletion or withdrawal procedure. |
| `AI-THREAT-012` | Candidate contamination | Scenario | Unreviewed AI output enters future training, search, indexes, source repositories, or evidence and appears authoritative. | Control themes | Quarantine; candidate namespace; admission state; index filtering; immutable provenance; cleanup and revalidation. |

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-SEC-AI-001,REQ-SEC-AI-002,REQ-SEC-AI-003,REQ-SEC-AI-004,REQ-SEC-AI-005,REQ-SEC-AI-006,REQ-SEC-AI-007,REQ-SEC-AI-008,REQ-SEC-AI-009,REQ-SEC-AI-010,REQ-SEC-AI-011,REQ-SEC-AI-012,REQ-SEC-AI-013,REQ-SEC-AI-014,REQ-SEC-AI-015,REQ-SEC-AI-016,REQ-SEC-AI-017,REQ-SEC-AI-018,REQ-SEC-AI-019,REQ-SEC-AI-020,REQ-SEC-AI-021,REQ-SEC-AI-022,REQ-SEC-AI-023,REQ-SEC-AI-024,REQ-SEC-AI-025,REQ-SEC-AI-026,REQ-SEC-AI-027,REQ-SEC-AI-028,REQ-SEC-AI-029,REQ-SEC-AI-030,REQ-SEC-AI-031,REQ-SEC-AI-032,REQ-SEC-AI-033,REQ-SEC-AI-034,REQ-SEC-AI-035,REQ-SEC-AI-036,REQ-SEC-AI-037,REQ-SEC-AI-038,REQ-SEC-AI-039,REQ-SEC-AI-040,REQ-SEC-AI-041,REQ-SEC-AI-042 -->
- **REQ-SEC-AI-001 — SHALL:** The global kOA baseline contains no native generative model, classifier, summarizer, embedding model, autonomous routing model, autonomous agent, AI category generator, or AI ingestion decision.
- **REQ-SEC-AI-002 — SHALL:** Core authorization, governance, privilege, identity, artifact verification, activation, rollback, recovery, deterministic rendering, kOA Mediatheque ingestion, and minimum offline operation remain independent of AI and UCKK availability.
- **REQ-SEC-AI-003 — SHALL:** The canonical external-AI allowlist is owned by `contracts/system.contract.json#/ai_boundary/allowed_external_surfaces`.
- **REQ-SEC-AI-004 — SHALL NOT:** An external AI provider, model, local model runtime, or AI-capable integration is enabled merely because software, credentials, network access, or a compatible API is present.
- **REQ-SEC-AI-005 — SHALL:** Every external AI operation is initiated by an explicit user or accountable workflow action after the exact purpose, provider, data, destination, output use, and material risks are presented.
- **REQ-SEC-AI-006 — SHALL:** Every AI capability is scoped by operation, data classification, source objects, destination, tools, network, retention, output use, duration, resource limits, and required review.
- **REQ-SEC-AI-007 — SHALL:** Data marked no-AI or otherwise ineligible remains outside external AI request, upload, retrieval, logging, caching, training, inference, and support paths.
- **REQ-SEC-AI-008 — SHALL:** Personal, sensitive, restricted, secret, culturally governed, or private operational data leaves the local or tenant domain only through an explicit compatible authority and minimization decision.
- **REQ-SEC-AI-009 — SHALL:** The transfer preview identifies selected source objects, fields, attachments, transformations, classification, destination, provider, purpose, retention context, and irreversible-disclosure risk.
- **REQ-SEC-AI-010 — SHALL NOT:** Secrets, private keys, unrestricted credentials, privileged tokens, recovery material, hidden system prompts containing authority data, or unrelated tenant data are transferred to an AI surface.
- **REQ-SEC-AI-011 — SHALL:** External AI output returns as a separately identified non-authoritative candidate with provider, model or service identity when known, operation identity, input references, output identity, warnings, and provenance.
- **REQ-SEC-AI-012 — SHALL NOT:** AI output directly grants privilege, changes policy, approves exceptions, recognizes authority, activates releases, publishes public content, resolves cultural rights, or writes an authoritative component store.
- **REQ-SEC-AI-013 — SHALL:** An owning component validates, reviews, admits, rejects, or quarantines AI output through its normal candidate-input contract.
- **REQ-SEC-AI-014 — SHALL:** Schema, policy, signature, identity, compatibility, deterministic rendering, release, activation, and privilege gates remain deterministic and treat AI output only as untrusted candidate input.
- **REQ-SEC-AI-015 — SHALL:** AI-assisted summaries, translations, classifications, tags, mappings, extracted claims, media, presentations, commands, and recommendations preserve source references and expose their candidate status.
- **REQ-SEC-AI-016 — SHALL:** Material AI-assisted content receives the human, expert, steward, community, legal, linguistic, accessibility, privacy, or publication review required by the owning contract.
- **REQ-SEC-AI-017 — SHALL:** Prompt injection, indirect instruction, tool-use request, retrieved content, attachment, and generated code are treated as untrusted data rather than authority.
- **REQ-SEC-AI-018 — SHALL NOT:** An AI surface receives unrestricted tools, arbitrary shell access, direct databases, protected signing services, kOA Node Agent operations, or general network access.
- **REQ-SEC-AI-019 — SHALL:** Any permitted AI tool call uses an allowlisted schema, bounded arguments, independent authorization, deterministic validation, timeout, replay protection when applicable, and a classified receipt.
- **REQ-SEC-AI-020 — SHALL:** Provider, model, policy, endpoint, retention, or capability drift triggers compatibility and security re-evaluation before continued use.
- **REQ-SEC-AI-021 — SHALL:** AI request and response retention follows data minimization, classification, rights, consent, withdrawal, legal, and evidence policy rather than provider defaults alone.
- **REQ-SEC-AI-022 — SHALL:** Logs and evidence retain the minimum operation metadata needed for review and recourse without duplicating sensitive prompts, source documents, audio, images, or generated output unnecessarily.
- **REQ-SEC-AI-023 — SHALL:** External AI unavailability, quota exhaustion, provider refusal, model change, or network loss degrades only the assistive capability and preserves local deterministic workflows.
- **REQ-SEC-AI-024 — SHALL:** A provider or integration can be disabled and removed without loss of authoritative data, core workflows, local navigation, deterministic media ingestion, active language rendering, recovery, or credible exit.
- **REQ-SEC-AI-025 — SHALL:** ChatGPT use remains user initiated and external, and system data transfer occurs only through an explicit registered integration or a manual user-mediated process.
- **REQ-SEC-AI-026 — SHALL:** Suno and Gamma remain user-triggered external adapters whose outputs return through controlled re-import, provenance, review, and owning-component admission.
- **REQ-SEC-AI-027 — SHALL NOT:** Suno or Gamma be invoked automatically by kOA Mediatheque ingestion, indexing, classification, tagging, category generation, routing, publication, backup, or restore, or by UCKK publication.
- **REQ-SEC-AI-028 — SHALL:** The approved Ariane voice adapter returns a transcript or structured-command candidate that is resolved and authorized by local deterministic Ariane controls.
- **REQ-SEC-AI-029 — SHALL:** Ariane voice failure leaves keyboard, pointer, touch, menu, shortcut, accessibility, and deterministic local command operation available.
- **REQ-SEC-AI-030 — SHALL:** Sensitive Ariane actions require action-specific local confirmation after the candidate command is displayed or otherwise made reviewable.
- **REQ-SEC-AI-031 — SHALL:** SenTient remains an optional isolated task-activated workbench available only through compatible developer or build profiles.
- **REQ-SEC-AI-032 — SHALL NOT:** SenTient is treated as part of the default user baseline, an always-running service, an authority over canonical data, a privilege controller, or a requirement for offline core operation.
- **REQ-SEC-AI-033 — SHALL:** SenTient uses isolated dependencies, storage, service identities, temporary data, network access, CPU, memory, queue, concurrency, timeout, cancellation, and idle shutdown.
- **REQ-SEC-AI-034 — SHALL:** SenTient preserves alternatives, contradictions, uncertainty, method identity, source provenance, reviewer disposition, and non-authoritative status.
- **REQ-SEC-AI-035 — SHALL:** A future local model or AI-capable component requires an accepted decision, registered component or integration, profile membership, artifact contract, threat review, data policy, resource envelope, tests, evidence, and removal behavior before active use.
- **REQ-SEC-AI-036 — SHALL NOT:** A local model is trusted, private, deterministic, authoritative, or safe merely because inference occurs on a kOA-controlled node.
- **REQ-SEC-AI-037 — SHALL:** AI-generated software, configuration, policy text, schema, migration, grammar, navigation, or documentation is reviewed and validated under the same owner contracts as human-authored candidate material.
- **REQ-SEC-AI-038 — SHALL:** AI-assisted documentation changes obey the canonical registry-first, decision-closure, generated-file, profile-scope, validation-evidence, and identifier-retirement rules.
- **REQ-SEC-AI-039 — SHALL:** Incident response can suspend a provider, credential, model, integration, AI capability, candidate set, or affected output without disabling unrelated core functions.
- **REQ-SEC-AI-040 — SHALL:** Withdrawal, rights change, consent revocation, provider compromise, or discovered ineligible transfer triggers bounded containment, output review, downstream remediation, and evidence.
- **REQ-SEC-AI-041 — SHALL:** Every active AI-boundary claim maps to an allowed surface or registered integration, capability policy, data decision, owning component, profile, threat, test, evidence, exception, and current status.
- **REQ-SEC-AI-042 — SHALL:** Ordinary Markdown AI-boundary documentation uses registry, reference, structure, language, decision, requirement, lock, and traceability validation without an automatic file-content-hash requirement.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Register an external AI capability

1. Identify the proposed provider, endpoint, model or service, and capability.
2. identify the owning integration and output component.
3. classify intended data, tools, audience, retention, and destinations.
4. complete the threat review.
5. define operation, failure, incident, removal, and exit behavior.
6. define profile membership and network exposure.
7. define credentials and revocation.
8. define candidate artifact and provenance.
9. define deterministic validation and review.
10. define tests and evidence.
11. update the canonical allowlist only after all required authority resolves.

### 6.2 Start an AI operation

1. Authenticate the user or accountable workflow.
2. resolve tenant, environment, profile, provider, capability, and integration identity.
3. select source objects explicitly.
4. evaluate classification, no-AI, rights, consent, audience, purpose, and export restrictions.
5. minimize and transform the selected data.
6. create the exact transfer preview.
7. obtain explicit confirmation.
8. create the operation identity and evidence.
9. start the bounded external request.

### 6.3 Process the external response

1. Receive the response into quarantine or a candidate namespace.
2. verify provider, operation, media type, size, and structural limits.
3. reject unexpected tool requests or embedded instructions.
4. create the candidate artifact identity.
5. attach provenance and limitations.
6. run deterministic schema, safety, source, compatibility, and policy checks.
7. route to the required owner review.
8. keep authoritative stores unchanged.

### 6.4 Admit or reject a candidate

1. Identify the owning component and target artifact or record.
2. display candidate status, sources, provider, warnings, and transformations.
3. perform required human, expert, steward, community, legal, accessibility, privacy, linguistic, security, or publication review.
4. accept selected material through an explicit owner mutation.
5. assign a new owner-controlled revision or artifact identity.
6. preserve the external candidate and disposition relationship.
7. reject, quarantine, withdraw, or supersede the remainder.
8. record evidence.

### 6.5 Execute an AI-proposed tool action

1. Parse the proposed call as untrusted candidate data.
2. resolve the declared tool contract.
3. validate all arguments and targets.
4. authenticate the local requester and tool workload.
5. obtain a new operation-specific authorization.
6. display sensitive effects and request confirmation when required.
7. execute through the owning component or narrow privileged broker.
8. verify the result.
9. record a receipt.
10. return a bounded result to the AI surface only when eligible.

### 6.6 Use Ariane voice

1. The user activates the optional voice mode.
2. Ariane identifies the active provider and data-transfer boundary.
3. the user supplies audio for the current interaction.
4. the adapter returns a transcript or command candidate.
5. Ariane displays or speaks back the interpreted action.
6. Ariane resolves it deterministically.
7. sensitive actions receive local confirmation.
8. normal authorization and execution run.
9. audio and transcript retention follow the operation policy.
10. local navigation remains available after any failure.

### 6.7 Use Suno or Gamma

1. The user selects the source material and external adapter.
2. the system evaluates eligibility and rights.
3. the system prepares and previews the export.
4. the user confirms.
5. the external provider creates candidate output.
6. the system imports the output through a controlled artifact path.
7. kOA Mediatheque or another local owner captures provenance, rights, and user metadata.
8. the user reviews and admits or rejects it.
9. publication, if any, follows Publication Gateway or the applicable artifact lifecycle.

### 6.8 Run a SenTient task

1. Verify that the active profile includes SenTient.
2. create a task-scoped isolated workspace.
3. admit candidate corpora with provenance and rights.
4. freeze the method, inputs, and resource budget.
5. execute bounded research.
6. preserve alternatives, contradictions, and uncertainty.
7. create a non-authoritative candidate.
8. submit it to an accountable review workflow.
9. release compute and temporary resources.
10. archive or delete according to policy.

### 6.9 Disable or remove a provider

1. Suspend new requests.
2. revoke or disable provider credentials.
3. stop queues and bounded retries.
4. preserve required local evidence.
5. identify unreviewed candidate outputs.
6. quarantine, reject, or review affected candidates.
7. remove endpoint and network access.
8. verify that core local capabilities continue.
9. export or delete provider-specific retained data according to policy.
10. record removal evidence.

### 6.10 Respond to an AI incident

1. Identify the provider, model, integration, operation, inputs, outputs, tools, reviewers, and downstream admissions.
2. suspend the affected capability.
3. preserve classified evidence without spreading sensitive content.
4. revoke credentials or trust where applicable.
5. quarantine affected candidates and derivative outputs.
6. evaluate unauthorized transfers, rights, consent, publication, and authoritative mutations.
7. withdraw, supersede, correct, or revalidate downstream state.
8. notify competent owners and affected authorities.
9. restore only after compatibility and security review.
10. update tests, contracts, and residual risk.

## 7. Failure and Degradation

### 7.1 Provider unavailable

The external assistive capability becomes unavailable.

Local deterministic operation continues.

Queued requests are canceled or retained only within explicit bounds and are revalidated before later transfer.

### 7.2 Data ineligible

The transfer remains blocked.

The user receives a stable reason and local alternative when available.

The system does not silently redact enough data to change the user's intended meaning without review.

### 7.3 Unknown provider or model state

An unknown endpoint, incompatible model, changed retention policy, unverified identity, or stale integration state blocks new requests.

Previously admitted local artifacts retain their own lifecycle status.

### 7.4 Prompt injection detected

The request or response remains candidate data.

Tool use, secrets, authority, and system instructions remain unaffected.

The system can remove the malicious source from context or require review.

### 7.5 Invalid or unsafe response

Malformed, oversized, deceptive, unsupported, policy-incompatible, or unverifiable output remains quarantined or rejected.

No authoritative state changes.

### 7.6 Review unavailable

The candidate remains pending, quarantined, or rejected according to the owner contract.

The system does not treat elapsed time or provider confidence as approval.

### 7.7 Quota, cost, or resource pressure

New AI tasks stop or reduce before local authority, navigation, ingestion, rendering, evidence, withdrawal, rollback, and recovery.

The user receives an explicit assistive-capability status.

### 7.8 Voice failure

Ariane returns to deterministic local interaction.

No partially interpreted command executes.

Sensitive confirmation state does not transfer to a later request.

### 7.9 SenTient failure

The active task stops, preserves fixed inputs and diagnostics, and discards incomplete derived results.

Core system functions remain unaffected.

### 7.10 Credential or provider compromise

The integration is suspended and credentials are revoked or rotated.

Affected outputs and transfers undergo impact review.

No provider compromise is treated as a global kOA authority compromise unless the evidence supports that broader scope.

### 7.11 Rights or consent withdrawal

New AI use stops for the affected material.

Retained requests, responses, candidate artifacts, indexes, publications, and downstream derivatives follow the owning withdrawal and remediation contracts.

Historical evidence is minimized according to lawful policy.

### 7.12 Integration removal

Authoritative local data, admitted artifacts, provenance, workflows, and export remain available.

Provider-specific conveniences disappear without creating a core-data migration dependency.

## 8. Cross-Component Interactions

| Interaction | AI boundary | Owner outcome |
| --- | --- | --- |
| User or accountable workflow → external AI | Explicit purpose, selected data, preview, confirmation, scoped provider and capability | Candidate response only |
| External AI → owning component | Controlled import, provenance, schema and policy validation | Admit, reject, quarantine, or request review |
| ChatGPT → local workflow | Manual import or registered integration | Candidate text or structured artifact |
| Suno or Gamma → kOA Mediatheque | Controlled candidate admission, original preservation, rights and metadata | Candidate media receives local identity only after admission; UCKK publication remains separate |
| Ariane voice adapter → Ariane Runtime | Candidate transcript or command | Local deterministic resolution, confirmation, authorization, and execution |
| SenTient → Orgo or Kristal admission | Isolated research candidate with alternatives and provenance | Accountable review or independent artifact admission |
| External AI → GF Wordbench | Candidate grammar, terminology, or translation | Human linguistic review and new source revision |
| GF Wordbench → SemantiK | Deterministically compiled verified language pack | Independent runtime verification and activation |
| External AI → Publication Gateway | Candidate wording or transformation only after local owner admission | Publication Gateway still performs disclosure policy, review, bundle, and delivery |
| Governance Policy Runtime → AI integration | Operation-specific data, tool, destination, exception, and retention decision | Integration enforces obligations but does not decide policy |
| Identity and Trust → AI integration | User, workflow, provider, model, credential, tenant, reviewer, and revocation identity | Authentication remains distinct from authorization |
| Audit Broker ← AI boundary | Classified transfer, tool, review, admission, incident, and withdrawal evidence | Audit does not store unrestricted prompts by default or authorize actions |
| Resource Governor → AI tasks | Quota, queue, concurrency, timeout, cancellation, and idle shutdown | Resource decisions do not grant data or action authority |
| kOA Node Agent ← AI-proposed action | No direct path | Only a separately authorized local owner can invoke an allowlisted operation |
| Sovereignty Bundle → clean restore | Preserves admitted local artifacts and provenance, not provider dependence | Core restore succeeds without the provider |

## 9. Decision Closure and Prohibited Assumptions

### 9.1 Closed decisions

| Decision | Closed rule |
| --- | --- |
| `DEC-AI-001` | The baseline has no native AI dependency; approved external AI is explicit, optional, removable, and non-authoritative. |
| `DEC-SENT-001` | SenTient is an optional isolated task-activated workbench and not a canonical authority. |
| `DEC-ARI-001` | Ariane local navigation is deterministic; external voice is optional and returns a candidate command. |
| `DEC-MEDIATHEQUE-001` | kOA Mediatheque ingestion is deterministic; Suno and Gamma are user-triggered external adapters. |
| `DEC-UCKK-EXT-001` | UCKK is an external online learning and Mediatheque platform; neither directional bridge nor external AI owns local admission authority. |
| `DEC-LANG-001` | AI language suggestions remain candidate source; GF Wordbench compilation and SemantiK runtime stay deterministic and separate. |
| `DEC-KRISTAL-001` | AI-extracted or reconciled claims remain candidates until explicit epistemic review and recognition. |
| `DEC-AUTH-001` | AI cannot infer or grant authority, privilege, publication, release, activation, exception, or recovery rights. |
| `DEC-IDENT-001` | User, workflow, provider, model, credential, operation, candidate, reviewer, artifact, tenant, and authority identities remain distinct. |
| `DEC-DATA-001` | AI surfaces cannot directly write component authoritative stores. |
| `DEC-COMP-001` | AI output crosses component boundaries only through explicit candidate and owner contracts. |
| `DEC-GOV-001` | Governance Policy Runtime decides data, tools, destination, exception, and action authority. |
| `DEC-PRIV-001` | Data minimization, no-AI, rights, consent, audience, withdrawal, and selective evidence govern AI use. |
| `DEC-LIFE-001` | AI-assisted artifacts use normal verification, publication, activation, rollback, revocation, and evidence lifecycles. |

### 9.2 Prohibited assumptions

Authors, implementers, validators, operators, and AI agents do not assume that:

- kOA has a native model runtime;
- a local model is trusted because it is local;
- a provider is allowed because credentials exist;
- a named provider has an automated integration;
- the newest provider model is compatible;
- user authentication authorizes data transfer;
- public data is free of rights or retention constraints;
- internal data is safe to transfer;
- absence of a no-AI label grants permission;
- redaction always prevents re-identification;
- prompt text can grant tools or authority;
- model output is evidence;
- model confidence is validation;
- a transcript is an executable command;
- a generated summary is publication-ready;
- a generated translation is a compiled language artifact;
- a generated claim is recognized knowledge;
- generated media has resolved rights or attribution;
- AI-generated code is safe or dependency neutral;
- SenTient is part of `user_lightweight`;
- SenTient can write Kristal or Orgo stores;
- AI unavailability can block local navigation or recovery;
- provider removal can remove authoritative local data;
- one tenant's AI consent applies to another tenant;
- one operation's confirmation applies to later changed data;
- provider logs are kOA audit evidence;
- a provider deletion request proves every downstream copy was deleted;
- ordinary Markdown requires content hashes because AI assisted its drafting.

A new implementation-affecting AI capability remains inactive until canonical ownership, authority, profile membership, data policy, failure behavior, tests, evidence, and removal are closed.

## 10. Validation Criteria

| Validation group | Required tests |
| --- | --- |
| Global AI baseline and removability | `TEST-SYS-001`, `TEST-SYS-002`, `TEST-SYS-003`, `TEST-SYS-005`, `TEST-SYS-012`, `TEST-SYS-015`, `TEST-EXIT-008` |
| Data, privacy, rights, and audit | `TEST-SEC-005`, `TEST-SEC-009`, `TEST-SEC-011`, `TEST-SEC-012`, `TEST-SEC-013`, `TEST-SEC-014`, `TEST-OPS-002`, `TEST-OPS-007`, `TEST-OPS-009` |
| Authority and component boundaries | `TEST-SYS-004`, `TEST-SYS-011`, `TEST-SYS-013`, `TEST-CROSS-004`, `TEST-CROSS-007`, `TEST-CROSS-008`, `TEST-CROSS-009`, `TEST-CROSS-013`, `TEST-CROSS-014`, `TEST-CROSS-015`, `TEST-SEC-001`, `TEST-SEC-002`, `TEST-SEC-003`, `TEST-SEC-006` |
| Ariane voice boundary | `TEST-SYS-006`, `TEST-CROSS-011`, `TEST-COMP-ARIANE-004`, `TEST-COMP-ARIANE-005`, `TEST-COMP-ARIANE-006`, `TEST-COMP-ARIANE-007`, `TEST-COMP-ARIANE-008`, `TEST-COMP-ARIANE-009` |
| kOA Mediatheque, UCKK, Suno, and Gamma boundary | `TEST-SYS-007`, `TEST-SYS-008`, `TEST-CROSS-003`, `TEST-CROSS-012`, `TEST-COMP-MEDIA-004`, `TEST-COMP-MEDIA-005`, `TEST-COMP-MEDIA-007`, `TEST-INT-UCKK-001`, `TEST-INT-UCKK-002` |
| SenTient isolation | `TEST-CROSS-006`, `TEST-PROF-004`, `TEST-PROF-005`, `TEST-PROF-006`, `TEST-PROF-008`, `TEST-PROF-010`, `TEST-OPS-003`, `TEST-OPS-006`, `TEST-OPS-010`, `TEST-COMP-SENTIENT-003`, `TEST-COMP-SENTIENT-004`, `TEST-COMP-SENTIENT-005`, `TEST-COMP-SENTIENT-006`, `TEST-COMP-SENTIENT-007`, `TEST-COMP-SENTIENT-008`, `TEST-COMP-SENTIENT-009` |
| Language and deterministic runtime | `TEST-SYS-009`, `TEST-CROSS-005`, `TEST-COMP-GFWB-004`, `TEST-COMP-GFWB-005`, `TEST-COMP-GFWB-007`, `TEST-COMP-GFWB-009`, `TEST-COMP-SEMANTIK-004`, `TEST-COMP-SEMANTIK-005`, `TEST-COMP-SEMANTIK-007`, `TEST-COMP-SEMANTIK-009` |
| Supply chain, recovery, and exit | `TEST-SEC-008`, `TEST-SEC-015`, `TEST-LIFE-003`, `TEST-LIFE-004`, `TEST-LIFE-005`, `TEST-LIFE-007`, `TEST-LIFE-008`, `TEST-LIFE-015`, `TEST-OPS-004`, `TEST-OPS-005`, `TEST-OPS-008`, `TEST-EXIT-001`, `TEST-EXIT-002`, `TEST-EXIT-003`, `TEST-EXIT-005`, `TEST-EXIT-006`, `TEST-EXIT-007` |
| AI-assisted documentation controls | `TEST-AI-DOC-001`, `TEST-AI-DOC-002`, `TEST-AI-DOC-003`, `TEST-AI-DOC-004`, `TEST-AI-DOC-005`, `TEST-AI-DOC-006`, `TEST-AI-DOC-007`, `TEST-AI-DOC-008`, `TEST-AI-DOC-009`, `TEST-AI-DOC-010`, `TEST-DOC-VAL-003`, `TEST-DOC-VAL-005`, `TEST-DOC-VAL-006`, `TEST-DOC-VAL-012`, `TEST-DOC-VAL-016`, `TEST-DOC-VAL-017`, `TEST-DOC-VAL-019`, `TEST-DOC-VAL-020` |

AI-boundary validation additionally confirms:

1. the global baseline declares no native generative, classification, summarization, embedding, routing, or autonomous-agent dependency;
2. every enabled external surface resolves in the canonical allowlist and integrations registry;
3. every operation has an authenticated initiator, explicit purpose, selected sources, data decision, destination, preview, confirmation, and expiry;
4. no-AI and restricted data controls apply to prompts, context, attachments, audio, images, retrieval, tools, logs, and support paths;
5. secrets, keys, privileged tokens, and unrelated tenant data remain absent;
6. outputs enter a candidate namespace with provenance;
7. owning-component admission is distinct from provider output;
8. no AI path directly reaches authoritative databases, signing, publication, activation, policy, or host privilege;
9. permitted tool calls use separate local authorization and bounded schemas;
10. ChatGPT, Suno, Gamma, and Ariane voice use their declared boundaries;
11. Ariane local navigation works without voice;
12. kOA Mediatheque ingestion remains deterministic and does not invoke Suno or Gamma automatically; UCKK publication remains independently authorized;
13. SenTient profile membership, isolation, resource limits, candidate status, and idle shutdown resolve;
14. GF Wordbench and SemantiK remain deterministic and separate;
15. provider drift, credential compromise, quota, network loss, and removal preserve core local operation;
16. rights and withdrawal remediation covers retained and admitted derivatives;
17. logs and evidence are classified and minimized;
18. AI-assisted development and documentation changes have executed validation evidence;
19. every requirement maps to an active test or approved manual control;
20. every active claim has current traceability and evidence;
21. exceptions are explicit, scoped, compensating, approved, and expiring;
22. no unresolved authority marker exists;
23. all active prose is in English.

A failed required test blocks or narrows the affected AI capability.

It does not create a claim that unrelated deterministic capabilities are unavailable.

## 11. Non-Normative Examples

### 11.1 ChatGPT drafting

A user selects an eligible public project description and opens a registered ChatGPT drafting operation.

The preview shows the exact text, provider, purpose, and output use. The user confirms. The response returns as a candidate draft with provenance.

The user edits and admits selected wording through the owning content workflow.

### 11.2 Separate manual ChatGPT use

A user consults ChatGPT outside kOA.

The user copies selected output into a local candidate field. kOA records that the source is an external user-provided candidate when provenance is relevant.

No system database or private evidence is uploaded automatically.

### 11.3 Suno media candidate

A user selects eligible lyrics and a generation purpose.

The kOA Mediatheque exports only approved material after rights review. Suno returns an audio candidate. The kOA Mediatheque imports the file, preserves the returned original, captures provenance and rights metadata, and waits for user admission. A later UCKK publication, if requested, follows the separate bridge.

The candidate is not public merely because it was generated.

### 11.4 Gamma presentation candidate

A user exports an approved public outline to Gamma.

The returned presentation enters a controlled import path. The user reviews factual claims, images, attribution, accessibility, and private-data leakage.

Publication Gateway handles any later private-to-public disclosure.

### 11.5 Ariane voice command

A user activates voice mode and says, “Export this case.”

The voice adapter returns a transcript candidate. Ariane maps it to an export command, displays the exact case, destination, data classes, and effects, and requests local confirmation.

The export runs only after normal authorization.

### 11.6 Prompt injection in a source document

A retrieved document contains instructions to reveal secrets and publish the result.

The content remains an untrusted source object. It does not change the operation contract or tool allowlist.

The candidate response is validated and reviewed normally.

### 11.7 SenTient reconciliation

SenTient proposes that two identifiers refer to the same entity.

The output preserves both alternatives, supporting and contradicting sources, method identity, and uncertainty. Orgo creates an accountable review task.

Kristal changes only after independent admission.

### 11.8 AI-generated grammar suggestion

An external surface proposes a French terminology change.

GF Wordbench imports it as candidate source, and a language reviewer evaluates semantics, regional usage, rights, and ambiguity. A new source revision is compiled and validated deterministically.

SemantiK receives only the verified language pack.

### 11.9 Provider drift

An integration detects that a provider endpoint now reports a different model and retention policy.

New requests stop. Existing admitted local artifacts remain valid under their own lifecycle. The integration requires compatibility and policy review before re-enablement.

### 11.10 Provider removal

An organization disables all external AI integrations.

Credentials, endpoints, queues, and provider-specific retained data are removed according to policy. Local navigation, kOA Mediatheque ingestion, SemantiK rendering, Kristal query, Orgo workflow, governance, artifact verification, backup, restore, and export continue. UCKK publication becomes unavailable without affecting local media.
