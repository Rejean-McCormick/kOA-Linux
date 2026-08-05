<!-- KOA:DOC-META:BEGIN GENERATED
{
 "doc_id": "DOC-RECIPE-ULW-BAS-001",
 "document_class": "implementation_recipe",
 "status": "active",
 "language": "en",
 "layer": "recipe",
 "scope": [
 "user_lightweight"
 ],
 "canonical_refs": [
 "contracts/system.contract.json#/global_boundaries",
 "contracts/system.contract.json#/offline_baseline",
 "contracts/system.contract.json#/degradation_baseline",
 "contracts/system.contract.json#/resource_governance",
 "contracts/system.contract.json#/ariane",
 "contracts/system.contract.json#/ai_boundary",
 "contracts/system.contract.json#/release_and_artifact_identity",
 "generated/profile-catalog.json#/primary_profiles/user_lightweight",
 "contracts/profiles/user-lightweight.profile.json",
 "contracts/artifact-contracts/resource-envelope.schema.json#/envelopes/user_lightweight",
 "generated/component-catalog.json",
 "contracts/integration-types.contract.json",
 "contracts/artifact-classes.contract.json",
 "contracts/artifact-contracts/node-profile.schema.json",
 "generated/requirements-index.json",
 "generated/assertion-index.json",
 "generated/test-catalog.json",
 "generated/evidence-catalog.json",
 "generated/traceability.json"
 ],
 "decision_ids": [
 "DEC-SYS-001",
 "DEC-PROFILE-001",
 "DEC-DATA-001",
 "DEC-GOV-001",
 "DEC-SHELL-001",
 "DEC-CONTAINER-001",
 "DEC-K8S-001",
 "DEC-HW-001",
 "DEC-REL-001",
 "DEC-AI-001",
 "DEC-SENT-001",
 "DEC-UCKK-EXT-001",
 "DEC-ARI-001"
 ],
 "requirement_ids": [
 "REQ-RECIPE-ULW-BAS-001",
 "REQ-RECIPE-ULW-BAS-002",
 "REQ-RECIPE-ULW-BAS-003",
 "REQ-RECIPE-ULW-BAS-004",
 "REQ-RECIPE-ULW-BAS-005",
 "REQ-RECIPE-ULW-BAS-006",
 "REQ-RECIPE-ULW-BAS-007",
 "REQ-RECIPE-ULW-BAS-008",
 "REQ-RECIPE-ULW-BAS-009",
 "REQ-RECIPE-ULW-BAS-010",
 "REQ-RECIPE-ULW-BAS-011",
 "REQ-RECIPE-ULW-BAS-012",
 "REQ-RECIPE-ULW-BAS-013",
 "REQ-RECIPE-ULW-BAS-014",
 "REQ-RECIPE-ULW-BAS-015",
 "REQ-RECIPE-ULW-BAS-016",
 "REQ-RECIPE-ULW-BAS-017",
 "REQ-RECIPE-ULW-BAS-018",
 "REQ-RECIPE-ULW-BAS-019",
 "REQ-RECIPE-ULW-BAS-020",
 "REQ-RECIPE-ULW-BAS-021",
 "REQ-RECIPE-ULW-BAS-022",
 "REQ-RECIPE-ULW-BAS-023",
 "REQ-RECIPE-ULW-BAS-024"
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
 "LOCK-SENT-001",
 "LOCK-MEDIATHEQUE-001",
 "LOCK-MEDIATHEQUE-002",
 "LOCK-ARI-001",
 "LOCK-ARI-002",
 "LOCK-IMPL-001",
 "LOCK-IMPL-002"
 ],
 "exception_ids": [],
 "depends_on": [
 "DOC-CONST-003",
 "DOC-SYS-000",
 "DOC-SYS-010",
 "DOC-SEC-010",
 "DOC-OPS-007",
 "DOC-OPS-017",
 "DOC-ADR-012"
 ],
 "tags": [
 "recipe",
 "user-lightweight",
 "browser-shell",
 "local-first",
 "loopback",
 "offline",
 "service-worker",
 "accessibility",
 "resource-governance",
 "same-origin",
 "component-boundaries",
 "non-authoritative-ui"
 ]
}
KOA:DOC-META:END -->

# Browser-Based Application Shell

## 1. Purpose

This recipe defines a browser-based local application shell for the `user_lightweight` profile.

The shell provides one maintained navigation surface for profile-selected components without becoming a new domain owner, policy engine, identity provider, resource scheduler, privileged broker, release authority, or shared database layer.

The reference design uses a local origin, versioned static assets, a narrow browser-facing routing layer, component-owned APIs, explicit capability state, bounded browser storage, offline shell availability, and optional installation as a browser application.

The recipe favors a small local footprint and predictable failure behavior over a large always-running frontend platform.

## 2. Scope

This recipe applies to:

- a maintained browser used as the user interface;
- a local shell service serving static assets and session endpoints;
- an optional same-origin browser-facing gateway;
- component route discovery and navigation;
- Ariane local navigation and accessibility;
- local session management;
- static asset and service-worker caching;
- browser storage used for non-authoritative state;
- offline operation and visible deferred work;
- Resource Governor limits;
- optional rootless-container deployment;
- shell and gateway updates;
- component-specific capability health;
- explicit external integration actions.

It does not define component business logic, component databases, policy rules, trust roots, release approval, publication decisions, privileged host operations, or one mandatory web framework.

The default design is local-only. Remote browser access is a separate profile extension.

## 3. Canonical References

| Canonical reference | Recipe responsibility |
| --- | --- |
| `contracts/system.contract.json#/global_boundaries` | Profile, component, data, privilege, and implementation boundaries |
| `contracts/system.contract.json#/offline_baseline` | Local capability and deferred remote-work behavior |
| `contracts/system.contract.json#/degradation_baseline` | Fail-closed, capability-scoped, pressure, and compatibility behavior |
| `contracts/system.contract.json#/resource_governance` | Resource Governor and policy-runtime separation |
| `contracts/system.contract.json#/ariane` | Deterministic local navigation and optional external voice |
| `contracts/system.contract.json#/ai_boundary` | Explicit external integration and no native AI |
| `contracts/system.contract.json#/release_and_artifact_identity` | Compatible update, non-partial activation, and recovery |
| `contracts/profiles/user-lightweight.profile.json` | Exact profile membership, component set, implementation, and limits |
| `contracts/resource-envelopes.registry.json#/envelopes/user_lightweight` | CPU, memory, I/O, queue, cache, and task bounds |
| `generated/component-catalog.json` | Component identities and authoritative responsibilities |
| `contracts/integration-types.contract.json` | External ChatGPT, Suno, Gamma, and Ariane voice contracts |
| `contracts/artifact-contracts/node-profile.schema.json` | Node capability-state declaration |
| `docs/08-operations/17-user-lightweight-operations.md` | Operational envelope and one-heavy-job rule |
| `docs/08-operations/07-capability-degradation.md` | Capability state and restoration model |
| `docs/07-security/10-data-at-rest.md` | Browser cache, temporary data, logs, and credential protection |
| `docs/10-adrs/ADR-012-single-narrow-privileged-broker.md` | Privileged host-operation boundary |

## 4. Model and Responsibilities

### 4.1 Reference topology

`text
maintained browser
 |
 | same-origin HTTP requests
 v
local shell origin on loopback
 |-- versioned static assets
 |-- session endpoints
 |-- capability discovery
 `-- allowlisted browser-facing routes
 |
 +--> Konnaxion API
 +--> Orgo API
 +--> Kristal Runtime API
 +--> UCKK API
 +--> task and health APIs
 +--> explicit integration adapters
`

The shell origin can be a small native service or a rootless container. Component services can run natively or in containers according to the profile.

### 4.2 Topology responsibilities

| Element | Responsibility | Authority boundary |
| --- | --- | --- |
| Browser or installed browser application | Renders the shell, manages focus and navigation, and submits authenticated requests. | Owns no authoritative application data. |
| Local shell origin | Serves versioned static assets, session endpoints, capability discovery, and bounded routing. | Does not redefine component authorization or API semantics. |
| Browser-facing gateway | Routes only allowlisted versioned component APIs under one local origin. | Cannot aggregate source writes or bypass component checks. |
| Identity and Trust | Establishes local identity, session validity, trust, and revocation. | The browser does not become identity authority. |
| Resource Governor | Bounds the shell, workers, queues, caches, and component task admission. | Resource admission is separate from user authorization. |
| Ariane local navigation | Provides deterministic navigation and accessibility controls. | External voice remains optional and separate. |
| Owning components | Own data, commands, events, validation, and business-state transitions. | The shell is a client, not a shared domain layer. |
| kOA Node Agent | Performs profile-authorized sensitive host lifecycle operations when needed. | The shell cannot expose arbitrary privileged commands. |

### 4.3 Origin and transport

The default listener is loopback-only, such as `127.0.0.1` and `::1`.

A profile-assigned port avoids collision with other local services. The browser launcher resolves the configured origin rather than embedding a universal port.

Loopback use can rely on the browser's local secure-context treatment where supported. Any non-loopback exposure uses an explicitly trusted certificate, authenticated clients, firewall restrictions, host validation, origin validation, session protection, and a profile-owned exposure record.

The server rejects unrecognized `Host`, `Origin`, and forwarding headers.

### 4.4 Shell routes

| Route pattern | Purpose | Canonical source |
| --- | --- | --- |
| `/` | Shell frame, navigation, capability summary, and current-node status. | Static assets plus bounded capability read model. |
| `/apps/<component-id>` | Component-owned application surface loaded through a registered route descriptor. | Versioned component API or separately bundled module with explicit compatibility. |
| `/tasks` | Visible current, queued, completed, failed, and cancelled task state. | Owning-component task APIs and Resource Governor admission. |
| `/offline` | Connectivity state, deferred work, offline import, and locally available capabilities. | Offline baseline and component-specific queue contracts. |
| `/settings` | Local presentation, accessibility, language-view, and bounded integration preferences. | No direct editing of protected policy, trust, or component source state. |
| `/health` | Human-readable capability-specific health and recovery guidance. | Machine health remains available through registered endpoints. |

A route descriptor identifies component ID, route ID, display label, icon artifact, minimum shell version, API version, capability state, accessibility label, and offline behavior.

The route descriptor cannot grant component authority.

### 4.5 Session model

The recommended session uses a same-origin, script-inaccessible cookie containing a short-lived opaque session reference.

The server associates the reference with:

- authenticated identity;
- node and profile context;
- issued and expiry times;
- revocation state;
- allowed browser origin;
- authentication strength;
- selected user-interface preferences;
- recent reauthentication where an operation requires it.

State-changing requests use request-forgery protection and origin validation. Browser back, reload, duplicate tabs, and process restart do not replay a mutation silently.

### 4.6 Browser storage

| Storage surface | Permitted content | Control |
| --- | --- | --- |
| HTTP-only session cookie | Session reference or bounded authentication state. | Short-lived, same-origin, secure when transport permits, and inaccessible to script. |
| Memory | Current route, transient form state, and short-lived response data. | Cleared on reload; never relied upon as authoritative persistence. |
| IndexedDB | Explicitly approved non-authoritative offline read models and bounded deferred-request metadata. | Schema-versioned, origin-scoped, encrypted when classification requires it, and safely discardable. |
| Cache Storage | Versioned shell assets and declared cacheable responses. | No secrets, no unrestricted API mirroring, and complete namespace replacement. |
| Local storage | Only low-risk presentation preferences when required. | No credentials, protected content, authority decisions, or mutation queues. |
| URL and history | Route identity and non-sensitive navigation state. | No tokens, secrets, protected filters, or private record contents. |

Browser storage remains an optimization. Clearing it cannot delete authoritative component records.

### 4.7 Service worker and offline shell

A service worker is optional.

When included, it provides:

- locally available shell assets;
- versioned cache namespaces;
- deterministic asset selection;
- declared offline route behavior;
- bounded cache cleanup;
- controlled read-model caching;
- visible offline status.

It does not intercept privileged operations or invent successful mutation responses.

An offline navigation request that lacks a cached component surface resolves to an explicit unavailable state rather than a fabricated page.

### 4.8 Component interaction

The browser-facing gateway exposes only allowlisted versioned routes.

It preserves:

- caller identity;
- component target;
- request and correlation IDs;
- method and content type;
- expected state when required;
- timeout;
- response status and stable error code;
- component receipt reference.

It does not merge component databases or reinterpret business errors.

Cross-component screens use controlled read models or separate component requests. A screen-level composition is not a shared source of truth.

### 4.9 Accessibility and Ariane

The shell frame provides:

- skip links;
- deterministic tab order;
- visible focus;
- semantic landmarks;
- route and page titles;
- accessible names;
- keyboard-operable menus and dialogs;
- status announcements;
- error summaries;
- focus restoration after navigation;
- zoom and reflow;
- reduced motion;
- contrast-compatible themes;
- local shortcuts that can be inspected and changed.

Ariane local navigation uses the same route and command registry. External voice adds an optional input adapter and cannot become the only path to an operation.

### 4.10 Deployment modes

| Deployment mode | Status | Required controls |
| --- | --- | --- |
| Native local service | Recommended default | Bind loopback, run as an unprivileged account, use profile resource limits, and serve local bundled assets. |
| Rootless container | Permitted | Bind loopback, use a read-only image, explicit writable cache paths, no host privilege, and bounded CPU and memory. |
| Desktop launcher | Permitted convenience | Open the local origin in a maintained browser or application mode without changing authority. |
| Local network exposure | Profile extension only | Require TLS, authenticated clients, firewall rules, explicit bind addresses, revocation, and exposure evidence. |
| Kubernetes endpoint deployment | Not part of this recipe | The profile does not require Kubernetes and gains no conformance from it. |

The recipe does not require a desktop environment. A maintained browser can run under GNOME, KDE Plasma, another standard environment, or a profile-selected shell.

### 4.11 Resource model

The shell uses:

- one small local service process;
- bounded static assets;
- lazy route loading;
- bounded response sizes;
- bounded browser caches;
- no permanent background synchronization loop;
- no permanent heavy search or enrichment process;
- task-activated component workers;
- profile-wide one-heavy-job admission.

The shell can prefetch a small declared route set only while Resource Governor and connectivity state permit it.

### 4.12 External integrations

ChatGPT, Suno, Gamma, and Ariane voice appear as optional explicit actions.

Before transfer, the shell shows:

- provider;
- purpose;
- selected data;
- classification and disclosure warning;
- expected output type;
- cancellation behavior;
- provenance behavior;
- local destination.

Returned material remains candidate input until the owning component accepts it.

### 4.13 Localization

Runtime interface localization is permitted through separate localization artifacts.

Canonical route IDs, operation IDs, capability states, stable error codes, component IDs, and source-document links remain unchanged.

The active recipe remains English according to .

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-RECIPE-ULW-BAS-001,REQ-RECIPE-ULW-BAS-002,REQ-RECIPE-ULW-BAS-003,REQ-RECIPE-ULW-BAS-004,REQ-RECIPE-ULW-BAS-005,REQ-RECIPE-ULW-BAS-006,REQ-RECIPE-ULW-BAS-007,REQ-RECIPE-ULW-BAS-008,REQ-RECIPE-ULW-BAS-009,REQ-RECIPE-ULW-BAS-010,REQ-RECIPE-ULW-BAS-011,REQ-RECIPE-ULW-BAS-012,REQ-RECIPE-ULW-BAS-013,REQ-RECIPE-ULW-BAS-014,REQ-RECIPE-ULW-BAS-015,REQ-RECIPE-ULW-BAS-016,REQ-RECIPE-ULW-BAS-017,REQ-RECIPE-ULW-BAS-018,REQ-RECIPE-ULW-BAS-019,REQ-RECIPE-ULW-BAS-020,REQ-RECIPE-ULW-BAS-021,REQ-RECIPE-ULW-BAS-022,REQ-RECIPE-ULW-BAS-023,REQ-RECIPE-ULW-BAS-024 -->
- **REQ-RECIPE-ULW-BAS-001 — SHALL:** The browser application shell shall be deployed only for the active `user_lightweight` profile or an explicitly compatible profile composition.
- **REQ-RECIPE-ULW-BAS-002 — SHALL:** The default application origin shall bind to loopback only and shall not accept non-local connections unless an explicit profile extension supplies authentication, transport security, firewall, and exposure policy.
- **REQ-RECIPE-ULW-BAS-003 — SHALL NOT:** The shell shall not become an authority for component data, policy, identity, resource admission, release approval, publication, privileged host mutation, or conformance.
- **REQ-RECIPE-ULW-BAS-004 — SHALL:** Every component interaction shall use a registered versioned API, command, event, gateway, exported artifact, or controlled read model owned by the component.
- **REQ-RECIPE-ULW-BAS-005 — SHALL NOT:** The shell, local reverse proxy, browser process, or service worker shall write directly to a component's authoritative database or source tables.
- **REQ-RECIPE-ULW-BAS-006 — SHALL:** The browser session shall use authenticated same-origin requests, bounded session lifetime, origin and request-forgery protection, and secure credential handling appropriate to the selected transport.
- **REQ-RECIPE-ULW-BAS-007 — SHALL NOT:** Long-lived bearer tokens, private keys, recovery secrets, or equivalent credentials shall be stored in browser local storage, ordinary IndexedDB records, URLs, logs, or client-visible configuration.
- **REQ-RECIPE-ULW-BAS-008 — SHALL:** The shell shall enforce a restrictive content security policy, prevent untrusted script execution, escape rendered content, and prohibit runtime dependency on unapproved third-party scripts or public content-delivery networks.
- **REQ-RECIPE-ULW-BAS-009 — SHALL:** Static shell assets shall be content-addressed or versioned, integrity-verified, locally available, and activated as one compatible set without partial browser-cache state.
- **REQ-RECIPE-ULW-BAS-010 — SHALL:** A service worker, when used, shall cache only declared assets and non-authoritative read data, shall use versioned cache namespaces, and shall remove superseded cache entries after compatible activation.
- **REQ-RECIPE-ULW-BAS-011 — SHALL NOT:** The service worker shall queue authoritative mutations unless the owning operation contract explicitly declares bounded, visible, idempotent, expiring, cancellable, and revalidated deferred execution.
- **REQ-RECIPE-ULW-BAS-012 — SHALL:** Offline mode shall preserve local navigation, cached shell assets, locally admitted component capabilities, capability status, and recovery guidance while marking unavailable external capabilities separately.
- **REQ-RECIPE-ULW-BAS-013 — SHALL:** Ariane local keyboard, pointer, touch, menu, shortcut, deterministic-command, focus, and accessibility navigation shall remain usable without external AI, voice, or network access.
- **REQ-RECIPE-ULW-BAS-014 — SHALL:** The shell shall meet declared keyboard, focus-order, semantic-structure, contrast, zoom, reduced-motion, screen-reader, error-identification, and status-announcement criteria.
- **REQ-RECIPE-ULW-BAS-015 — SHALL:** The shell shall display capability-specific states including enabled, degraded, read-only, inspection-only, blocked, unavailable, recovering, disabled, and not-applicable where those states are returned by active contracts.
- **REQ-RECIPE-ULW-BAS-016 — SHALL:** Resource Governor shall bound the shell service, browser-facing gateway, caches, workers, synchronization, previews, indexing requests, and retained diagnostics within the `user_lightweight` envelope.
- **REQ-RECIPE-ULW-BAS-017 — SHALL:** The shell shall start heavy work only through the owning component's task interface and shall preserve the profile-wide one-heavy-job admission rule.
- **REQ-RECIPE-ULW-BAS-018 — SHALL:** Containers shall remain optional, the application contract shall remain runtime-neutral, and the recipe shall not require Kubernetes.
- **REQ-RECIPE-ULW-BAS-019 — SHALL:** External ChatGPT, Suno, Gamma, and Ariane voice actions shall require explicit user initiation, visible data selection, capability-scoped consent, and candidate-output handling.
- **REQ-RECIPE-ULW-BAS-020 — SHALL NOT:** The shell shall invoke native or external AI automatically for navigation, ingestion, classification, summarization, translation, routing, tagging, authority, recovery, or background enrichment.
- **REQ-RECIPE-ULW-BAS-021 — SHALL:** Shell logs, client telemetry, health output, crash reports, receipts, and diagnostics shall be bounded, minimized, free of secrets, and disabled for external transmission unless explicitly authorized.
- **REQ-RECIPE-ULW-BAS-022 — SHALL:** Shell and browser-facing gateway updates shall verify artifact identity, integrity, profile compatibility, API compatibility, recovery capacity, and previous valid assets before activation.
- **REQ-RECIPE-ULW-BAS-023 — SHALL:** Restoration after shell, cache, session, component, network, or update failure shall revalidate identity, origin, profile, API versions, capability state, queued work, resources, and asset integrity before full readiness returns.
- **REQ-RECIPE-ULW-BAS-024 — SHALL:** Every active browser-shell, origin, session, cache, offline, accessibility, resource, update, and conformance claim shall be traceable to accepted decisions, active requirements, applicable locks, registered tests, and valid evidence.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Implementation Procedure

### 6.1 Create the shell artifact

1. Select one maintained frontend build system.
2. produce static versioned assets;
3. generate an asset manifest with content identities;
4. define the shell route registry;
5. define browser-storage schemas and quotas;
6. define service-worker behavior or explicitly omit it;
7. define accessibility acceptance tests;
8. package assets as a registered services artifact;
9. record supported component API versions;
10. retain a previous valid asset set.

### 6.2 Configure the local origin

1. Allocate the profile-owned local port.
2. bind IPv4 and IPv6 loopback only;
3. reject unrecognized hosts and forwarding headers;
4. configure same-origin session endpoints;
5. configure request-forgery and origin validation;
6. configure restrictive security headers;
7. disable directory listing and arbitrary file serving;
8. expose only declared health and application routes;
9. apply process and resource limits;
10. verify no non-local listener exists.

### 6.3 Configure security headers

Use a policy equivalent to:

`text
default-src 'self';
script-src 'self';
style-src 'self';
img-src 'self' data: blob:;
font-src 'self';
connect-src 'self';
object-src 'none';
base-uri 'none';
frame-ancestors 'none';
form-action 'self';
manifest-src 'self';
worker-src 'self' blob:;
`

The selected implementation can tighten this policy further.

Inline script and runtime-evaluated code are omitted. Any unavoidable exception is explicit, bounded, reviewed, and tested.

### 6.4 Register component routes

1. Resolve the component ID and owner.
2. resolve the versioned browser API;
3. define route and capability IDs;
4. define required identity and authorization;
5. define offline and degraded behavior;
6. define API and shell compatibility;
7. define maximum response and upload sizes;
8. define stable error handling;
9. define accessibility labels;
10. add positive and negative route tests.

### 6.5 Configure session handling

1. Authenticate through the profile's Identity and Trust flow.
2. create a short-lived server-side session;
3. issue a script-inaccessible same-origin cookie;
4. bind the session to node, profile, origin, and expiry;
5. issue request-forgery material through a protected flow;
6. rotate or revoke sessions as required;
7. require reauthentication for declared sensitive actions;
8. clear server and browser session state on logout;
9. preserve only non-sensitive unsent form state when safe.

### 6.6 Configure offline behavior

1. Cache the complete compatible shell asset set.
2. declare cacheable read models;
3. define cache version and quota;
4. define unavailable route behavior;
5. define eligible deferred requests;
6. expose connectivity and queue state;
7. revalidate identity, authorization, expected state, compatibility, and expiry after reconnection;
8. remove superseded caches after successful activation;
9. test a cold offline start and an online-to-offline transition.

### 6.7 Configure task activation

1. Route heavy work to the owning component.
2. request Resource Governor admission;
3. expose expected resource and temporary-storage use;
4. respect the one-heavy-job limit;
5. show queue, progress, cancellation, and failure state;
6. stop frontend polling when the route is hidden or the operation completes;
7. validate the result through the owning component;
8. retain only bounded task history.

### 6.8 Configure updates

1. Download or import the candidate services artifact.
2. verify identity, integrity, trust, profile, shell, component API, and browser compatibility;
3. preserve the previous asset and gateway set;
4. stage under a new version namespace;
5. warm only declared assets;
6. activate the shell and service worker as a compatible set;
7. verify route, session, API, accessibility, offline, and health checks;
8. commit the candidate;
9. restore the previous set on failure;
10. clean superseded caches after retention conditions pass.

### 6.9 Configure optional rootless container deployment

1. Use a versioned read-only image.
2. run as a non-root identity;
3. bind loopback only;
4. expose no container-management socket;
5. grant no host devices or broad capabilities;
6. mount only explicit configuration and cache paths;
7. apply CPU, memory, process, and storage limits;
8. keep component data outside the shell container;
9. verify native and container deployments satisfy the same application contract.

### 6.10 Operate and maintain

1. Monitor capability-specific health rather than process status alone.
2. keep logs and retained browser diagnostics bounded;
3. clear superseded caches;
4. review failed authentication and security-policy events;
5. test offline operation;
6. test session revocation;
7. test component failure containment;
8. test update rollback;
9. test accessibility with keyboard and assistive technology;
10. review resource use under the minimum hardware envelope.

## 7. Failure States and Safe Degradation

| Failure state | Required response | Preserved state | Blocked behavior |
| --- | --- | --- | --- |
| Shell service unavailable | Report the shell unavailable and preserve component state; restart through the ordinary service lifecycle. | Component-owned data and background tasks | Assuming component failure |
| Browser cache corrupt or incompatible | Discard the affected namespace and load the last valid local asset set. | Server-side and component state | Mixed asset versions |
| Service worker activation fails | Keep the previous worker active and mark the candidate update blocked. | Previous valid shell | Partial cache activation |
| Session expires or is revoked | Block protected requests, preserve unsent local form state when safe, and require reauthentication. | Public shell frame and non-sensitive preferences | Background mutation |
| Component API unavailable | Mark only that component capability unavailable or degraded. | Other routes and components | Silent substitute API |
| API version incompatible | Block the affected route or action and retain compatible assets. | Other compatible capabilities | Schema guessing |
| Network unavailable | Preserve local shell assets and declared local capabilities; show bounded deferred work. | Local navigation and admitted local data | Automatic external fallback |
| Resource pressure | Stop prefetch, background refresh, previews, and optional workers; reduce cache and concurrency. | Navigation, active form integrity, and recovery | Unbounded browser work |
| Heavy job already active | Queue visibly or reject according to the owning task contract. | Current heavy job and ordinary shell use | Second concurrent heavy job |
| External AI or media provider unavailable | Disable only the selected external action. | All unrelated local routes | Provider substitution |
| Content security violation | Block the resource or execution, record bounded diagnostics, and preserve the last valid shell. | Local assets and component data | Relaxing policy automatically |
| Local storage or IndexedDB unavailable | Operate without optional cached views and block offline actions that require them. | Online component interaction | Treating browser storage as authoritative |
| Privileged lifecycle action requested | Use a registered component flow that reaches the narrow privileged broker when authorized. | Shell authority boundary | Direct shell or browser privilege |
| Update health check fails | Restore the previous shell and gateway artifact set. | Previous valid UI and API compatibility | Keeping a partially healthy candidate |

The shell never reports a protected action as successful unless the owning component returns a valid result.

A frontend display failure does not roll back or reinterpret a completed component transaction. The shell refreshes the authoritative component state using the request or receipt identity.

## 8. Cross-Component Interactions

| Producer or owner | Browser shell use | Boundary |
| --- | --- | --- |
| User-lightweight profile | Selects the shell, routes, components, resources, connectivity, and exposure | Recipe cannot expand profile membership |
| Identity and Trust | Supplies authentication, session validity, trust, and revocation | Shell does not mint authority |
| Resource Governor | Admits tasks and bounds services, browser workers, caches, and queues | Shell cannot override resource denial |
| Governance Policy Runtime | Supplies policy decisions where the profile explicitly deploys it | Shell does not infer policy from UI state |
| Konnaxion | Supplies component-owned coordination views and commands | Shell cannot write Konnaxion source tables |
| Orgo | Supplies component-owned organizational views and commands | Shell cannot merge Orgo ownership into navigation state |
| Kristal Runtime | Supplies admitted language-runtime capability | Shell does not become a language-construction workbench |
| UCKK | Supplies deterministic media, metadata, export, backup, and restore operations | Heavy work remains task-activated and serialized |
| Ariane | Supplies deterministic local navigation and optional external voice input | Voice does not replace local navigation |
| External integration adapters | Perform explicit selected external operations | Outputs remain candidate input |
| Audit Broker | Records selective security, access, and critical-transition evidence | Shell telemetry does not become audit authority |
| kOA Node Agent | Performs registered sensitive host mutations | Shell exposes no arbitrary privileged interface |
| Release workflow | Supplies compatible versioned shell and gateway artifacts | Local success does not create release authority |

## 9. Decision Closure and Prohibited Assumptions

### Accepted decisions

| Decision ID | Closed question |
| --- | --- |
| `DEC-SYS-001` | The shell remains a modular local client within explicit authority boundaries. |
| `DEC-PROFILE-001` | Browser-shell membership and exposure remain profile-scoped. |
| `DEC-DATA-001` | The shell and gateway cannot own or write component source data directly. |
| `DEC-GOV-001` | Resource admission and policy authorization remain separate. |
| `DEC-SHELL-001` | A maintained browser-based shell is a profile implementation choice. |
| `DEC-CONTAINER-001` | Native and rootless-container deployments remain contract-equivalent. |
| `DEC-K8S-001` | Kubernetes is not an endpoint requirement. |
| `DEC-HW-001` | The shell operates within the lightweight hardware and one-heavy-job envelope. |
| `DEC-REL-001` | Shell assets and gateway versions use compatible non-partial activation and recovery. |
| `DEC-AI-001` | External AI remains explicit and non-authoritative; native AI is absent. |
| `DEC-SENT-001` | SenTient is excluded from the default user installation. |
| `DEC-UCKK-EXT-001` | Local Mediatheque interaction and accepted UCKK learning packages remain available without implicit online synchronization. |
| `DEC-ARI-001` | Local navigation remains independent of voice and external AI. |

### Prohibited assumptions

- A single browser origin is a single data owner.
- The shell can authorize an operation because it rendered the button.
- A hidden button is an access-control mechanism.
- Browser process ownership proves user identity.
- Loopback removes the need for authentication and origin checks.
- Local storage is safe for credentials.
- IndexedDB is an authoritative application database.
- A service worker can acknowledge mutations while offline.
- Browser cache freshness proves component-state freshness.
- A reverse proxy can rewrite component authorization.
- A valid session permits every component action.
- A successful component response permits cross-component source writes.
- A local administrator can bypass component authority through browser tools.
- A desktop launcher grants privileged host access.
- Container deployment is required or inherently safer.
- Kubernetes improves endpoint conformance.
- External AI can run automatically in the background.
- Voice can become the only navigation mechanism.
- A process being alive means every route is ready.
- Reconnection validates queued work automatically.
- Resource pressure permits a second heavy job.
- Localized interface text can change canonical IDs or operation meaning.
- Clearing browser storage can delete authoritative component data.
- Missing compatibility evidence can be replaced by manual browser testing.

## 10. Validation Criteria

1. The metadata block parses as JSON and declares `DOC-RECIPE-ULW-BAS-001`, status `active`, language `en`, recipe layer, and `user_lightweight` scope.
2. All eleven required sections exist in numerical order.
3. Every decision ID is accepted in the system decision registry.
4. Every requirement ID appears exactly once in the requirements registry after registry generation.
5. Every lock ID resolves to an active lock after registry generation.
6. The following recipe tests are registered and pass:

| Test ID | Purpose |
| --- | --- |
| `TEST-RECIPE-ULW-BAS-001` | Verify exact `user_lightweight` profile applicability and overlay compatibility. |
| `TEST-RECIPE-ULW-BAS-002` | Verify loopback-only default binding and rejection of non-local connections. |
| `TEST-RECIPE-ULW-BAS-003` | Verify optional network exposure requires TLS, authentication, firewall, revocation, and profile authorization. |
| `TEST-RECIPE-ULW-BAS-004` | Verify shell non-authority and absence of direct component database access. |
| `TEST-RECIPE-ULW-BAS-005` | Verify allowlisted versioned component routes and component-side authorization. |
| `TEST-RECIPE-ULW-BAS-006` | Verify session expiry, revocation, request-forgery protection, origin validation, and credential storage rules. |
| `TEST-RECIPE-ULW-BAS-007` | Verify content security policy, script integrity, escaping, frame restrictions, and absence of unapproved remote scripts. |
| `TEST-RECIPE-ULW-BAS-008` | Verify atomic static-asset and service-worker cache activation and rollback. |
| `TEST-RECIPE-ULW-BAS-009` | Verify browser storage classes, quotas, schema migration, clearing, and absence of secrets. |
| `TEST-RECIPE-ULW-BAS-010` | Verify local navigation and declared local capabilities without network, voice, or external AI. |
| `TEST-RECIPE-ULW-BAS-011` | Verify bounded visible idempotent deferred work and revalidation after reconnection. |
| `TEST-RECIPE-ULW-BAS-012` | Verify keyboard, focus, semantics, contrast, zoom, reduced motion, screen-reader, and live-status behavior. |
| `TEST-RECIPE-ULW-BAS-013` | Verify capability-specific enabled, degraded, read-only, inspection-only, blocked, unavailable, recovering, disabled, and not-applicable states. |
| `TEST-RECIPE-ULW-BAS-014` | Verify Resource Governor limits and one-heavy-job admission. |
| `TEST-RECIPE-ULW-BAS-015` | Verify optional container deployment, runtime neutrality, and absence of Kubernetes requirement. |
| `TEST-RECIPE-ULW-BAS-016` | Verify explicit external integration invocation, data preview, consent, provenance, and candidate-output handling. |
| `TEST-RECIPE-ULW-BAS-017` | Verify absence of native or external AI background invocation and authority. |
| `TEST-RECIPE-ULW-BAS-018` | Verify bounded secret-free logs, diagnostics, crash reports, and external telemetry defaults. |
| `TEST-RECIPE-ULW-BAS-019` | Verify compatible shell and gateway update, previous-valid rollback, and restoration revalidation. |
| `TEST-RECIPE-ULW-BAS-020` | Verify complete traceability to decisions, requirements, locks, profile, components, tests, and evidence. |

7. Active prose is English and contains no unresolved marker, draft state, metadata hash, or source hash.
8. The generated requirement block matches the canonical requirements registry.
9. Validation evidence identifies the profile, browser, shell artifact, gateway artifact, origin, transport, component API versions, cache version, resource envelope, tests, and result.

These criteria define the recipe validation target. They do not claim that a particular browser, framework, local port, container image, component bundle, or installation already conforms.

## 11. Non-Normative Example Configuration

The following example illustrates one local deployment. It is not a canonical profile or release artifact.

`yaml
shell:
 profile: user_lightweight
 listen:
 addresses:
 - 127.0.0.1
 - ::1
 port: 8765
 remote_access: false
 assets:
 version: example-shell-1.0.0
 manifest: /usr/share/koa-shell/asset-manifest.json
 previous_version_retained: true
 session:
 cookie_name: koa_shell_session
 http_only: true
 same_site: strict
 lifetime_minutes: 30
 request_forgery_protection: true
 browser_storage:
 local_storage:
 allowed:
 - theme
 - reduced_motion
 indexed_db:
 quota_mib: 128
 authoritative: false
 cache_storage:
 quota_mib: 256
 versioned_namespaces: true
 service_worker:
 enabled: true
 cache_mutations: false
 cache_external_integrations: false
 resources:
 memory_limit_mib: 384
 worker_concurrency: 2
 heavy_job_concurrency: 1
 routes:
 - component_id: konnaxion
 route: /apps/konnaxion
 offline: declared_by_component
 - component_id: orgo
 route: /apps/orgo
 offline: declared_by_component
 - component_id: uckk
 route: /apps/uckk
 offline: declared_by_component
 external_integrations:
 automatic_invocation: false
 require_data_preview: true
 telemetry:
 external_export_enabled: false
`

A desktop launcher can open `http://127.0.0.1:8765/` in application mode. The exact port, browser, service manager, framework, and packaging mechanism remain profile and implementation choices.
