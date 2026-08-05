<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SEC-008",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "security",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/system.contract.json",
    "generated/component-catalog.json",
    "contracts/integration-types.contract.json"
  ],
  "decision_ids": [
    "DEC-SEC-001",
    "DEC-COMP-001",
    "DEC-INT-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-GATE-001",
    "DEC-OFFLINE-001",
    "DEC-PROFILE-001",
    "DEC-AI-001",
    "DEC-SENT-001",
    "DEC-CONTAINER-001",
    "DEC-K8S-001"
  ],
  "requirement_ids": [
    "REQ-SEC-NET-001",
    "REQ-SEC-NET-002",
    "REQ-SEC-NET-003",
    "REQ-SEC-NET-004",
    "REQ-SEC-NET-005",
    "REQ-SEC-NET-006",
    "REQ-SEC-NET-007",
    "REQ-SEC-NET-008",
    "REQ-SEC-NET-009",
    "REQ-SEC-NET-010",
    "REQ-SEC-NET-011",
    "REQ-SEC-NET-012",
    "REQ-SEC-NET-013",
    "REQ-SEC-NET-014",
    "REQ-SEC-NET-015",
    "REQ-SEC-NET-016",
    "REQ-SEC-NET-017",
    "REQ-SEC-NET-018",
    "REQ-SEC-NET-019",
    "REQ-SEC-NET-020",
    "REQ-SEC-NET-021",
    "REQ-SEC-NET-022",
    "REQ-SEC-NET-023",
    "REQ-SEC-NET-024",
    "REQ-SEC-NET-025",
    "REQ-SEC-NET-026",
    "REQ-SEC-NET-027",
    "REQ-SEC-NET-028",
    "REQ-SEC-NET-029",
    "REQ-SEC-NET-030"
  ],
  "lock_ids": [
    "LOCK-SEC-001",
    "LOCK-SEC-002",
    "LOCK-SEC-003",
    "LOCK-SEC-004",
    "LOCK-SEC-005",
    "LOCK-SEC-006",
    "LOCK-SEC-007",
    "LOCK-SEC-008",
    "LOCK-SEC-009",
    "LOCK-SEC-010",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-GATE-001",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-SENT-001",
    "LOCK-OFFLINE-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-SEC-000",
    "DOC-SEC-001"
  ],
  "tags": [
    "security",
    "normative-markdown",
    "08",
    "network",
    "boundaries"
  ]
}
KOA:DOC-META:END -->

# Network Boundaries

## 1. Purpose

This document defines the security boundaries for network communication in kOA. It establishes how components, profiles, users, administrators, gateways, federation peers, external services, and recovery systems communicate without treating network location as identity or trust.

The network model is designed to:

- deny undeclared communication by default;
- separate public, private, governance, administration, federation, backup, development, and external-integration traffic;
- authenticate component and human identities independently from network placement;
- minimize exposed services and transferred data;
- preserve component data ownership;
- prevent direct database and internal-state access across component boundaries;
- keep local Mediatheque admission internal and external publication behind Publication Gateway;
- permit outbound UCKK delivery only through the gateway-authorized publication adapter;
- permit inbound UCKK learning packages only through the declared import endpoint or approved offline-bundle intake into quarantine;
- constrain outbound communication and external integrations;
- preserve local operation during Internet or upstream failure;
- make degraded connectivity and blocked authority visible;
- support profile-specific transports without changing global authority semantics.

A network path permits delivery only. It does not establish authorization, consent, cultural authority, publication authority, component ownership, or trust.

## 2. Scope

### 2.1 Covered communication

This document applies to:

- local process-to-process communication;
- Unix sockets;
- loopback interfaces;
- container networks;
- host networks;
- LAN communication;
- inter-node communication;
- remote administration;
- federation;
- artifact synchronization;
- publication delivery;
- external integrations;
- package and update retrieval;
- backup transfer;
- monitoring and audit forwarding;
- developer workspace services;
- Windows-to-WSL communication;
- recovery and break-glass network access.

The same authority rules apply whether communication occurs in one process, one host, one container runtime, one cluster, one site, or across the Internet.

### 2.2 Logical network zones

Profiles can implement the following logical zones:

| Zone | Purpose |
| --- | --- |
| `public` | Controlled Konnaxion-facing delivery and explicitly approved public endpoints. |
| `private` | Orgo and other protected user, tenant, workflow, or operational services. |
| `governance` | Identity, trust, policy, audit, consent, and publication-decision services. |
| `administration` | Operator access, health, maintenance, recovery, and narrow host operations. |
| `federation` | Explicit synchronization or artifact exchange with configured peers. |
| `backup` | Protected backup transfer and restore verification. |
| `development` | Workspace-scoped development services and local test traffic. |
| `external_integration` | Explicitly approved communication with external providers or surfaces. |
| `quarantine` | Inspection of untrusted or not-yet-accepted imports. |

A profile can collapse physical interfaces when equivalent logical separation, policy, identity, observation, and failure containment are demonstrated. A physical interface cannot collapse the authority distinctions.

### 2.3 Profile applicability

This document applies globally. Individual profiles determine which zones exist and how they are implemented.

Examples:

- a lightweight user endpoint can implement several logical zones on one host;
- a developer workstation can isolate each workspace through separate container or service namespaces;
- a sovereign hub can expose distinct public, private, governance, administration, federation, and backup interfaces;
- a sovereign Linux node can implement host-level enforcement;
- a high-assurance overlay can impose stronger segmentation and inspection controls.

No profile silently inherits a stronger or weaker network claim.

### 2.4 External and optional services

External AI, voice, creative, publication, identity, registry, update, federation, and backup services are outside the local trust boundary unless an active integration contract states otherwise.

Optional external connectivity does not become a baseline dependency. Failure of an optional service disables only that bounded capability.

### 2.5 Excluded authority

This document does not:

- grant identities;
- define trust roots;
- grant consent;
- approve publication;
- allocate component data ownership;
- define application payload semantics;
- define production topology for every profile;
- require one firewall technology;
- require containers;
- require Kubernetes;
- require a service mesh;
- require Internet access;
- replace component or integration contracts.

## 3. Canonical References

| Canonical reference | Responsibility |
| --- | --- |
| `contracts/system.contract.json` | Owns global network, offline, gateway, component, trust, and safe-degradation architecture. |
| `generated/component-catalog.json` | Owns component identities, responsibilities, authoritative data, and primary interfaces. |
| `contracts/integration-types.contract.json` | Owns registered integrations, participants, direction, transport class, data movement, and lifecycle. |

Supporting authority is owned by:

- component contracts under `contracts/components/`;
- profile contracts under `contracts/profiles/`;
- `generated/authority-manifest.json`;
- `generated/requirements-index.json`;
- `generated/assertion-index.json`;
- `generated/exception-index.json`;
- `generated/test-catalog.json`;
- `generated/evidence-catalog.json`;
- `contracts/release-channels.contract.json`;
- artifact and integration manifests under `contracts/artifact-contracts/`.

A profile or recipe can select an implementation mechanism. It does not redefine these global boundaries.

## 4. Model and Responsibilities

### 4.1 Network-boundary model

A network interaction is described by:

- source component or human identity;
- source zone;
- destination component or service identity;
- destination zone;
- operation class;
- direction;
- transport;
- authentication method;
- authorization scope;
- tenant or authority domain;
- purpose;
- data classification;
- payload contract;
- destination port or socket;
- retry and timeout policy;
- offline behavior;
- observability requirements;
- lifecycle state.

A route exists only when an active contract declares these properties.

### 4.2 Default-deny policy

Inbound and outbound communication is denied unless explicitly declared.

A declaration identifies the exact participants, operation, scope, transport, destination, and lifecycle. Broad rules such as unrestricted internal networks, unrestricted outbound HTTPS, or universal administrative access are not accepted as application contracts.

Temporary debugging access remains separate from the baseline and follows an approved, time-bounded exception or development-only contract.

### 4.3 Identity before location

The receiver validates the calling identity and scope even when the caller is:

- on loopback;
- on the same host;
- in the same container network;
- in the same Kubernetes namespace;
- on the same LAN;
- connected through a private address;
- using a valid certificate;
- operated by an administrator.

A source address, network name, namespace, certificate possession, or successful transport handshake contributes evidence but does not alone authorize the application operation.

### 4.4 Public and private separation

Public-facing services expose only bounded public interfaces.

Public services cannot directly access private component databases. Private state can reach a public domain only through a versioned component interface, declared event flow, verified artifact, or Publication Gateway as applicable.

Konnaxion public endpoints remain separate from Orgo private workflow state.

### 4.5 Governance-zone separation

Identity and Trust, Governance Policy Runtime, Audit Broker, and Publication Gateway expose narrow authenticated service interfaces.

Application components do not receive unrestricted access to governance databases or internal policy state.

Governance services can receive the minimum application context required for a decision. They do not become owners of application business data.

### 4.6 Administrative boundary

Administrative interfaces are separate from public and application interfaces.

Administrative access uses:

- strong human or service authentication;
- explicit administrator roles;
- narrow operations;
- restricted source networks or access brokers;
- short-lived sessions where supported;
- audit evidence;
- rate limits;
- safe timeout;
- revocation;
- recovery paths.

A host administrator does not automatically gain application, publication, consent, or cultural authority.

### 4.7 Local privileged interfaces

Node-local privileged operations prefer Unix sockets or equivalent local transports with operating-system access controls.

A privileged broker accepts only allowlisted operation identifiers and bounded parameters. It does not expose an arbitrary shell or unrestricted command forwarding interface.

### 4.8 Federation boundary

Federation is disabled until peers, trust scopes, tenants, environments, release channels, artifact classes, capabilities, and authorities are explicitly configured.

A peer signature proves possession of a recognized signing capability. It does not by itself authorize import, synchronization, publication, or activation.

Federation traffic enters validation or quarantine before authoritative acceptance.

### 4.9 External-integration boundary

External integrations use a registered integration manifest and explicit egress permission.

The boundary records:

- provider identity;
- destination;
- purpose;
- minimized payload;
- data classification;
- consent and authority;
- retention and reuse conditions;
- return path;
- acceptance path;
- deletion or termination capability;
- failure behavior.

An external response remains candidate input until accepted by the owning component.

### 4.10 Gateway boundaries

Publication Gateway mediates governed cross-domain publication.

The kOA Mediatheque mediates controlled local admission of user-selected media. Publication Gateway with the UCKK adapter mediates controlled outbound publication to the external Moodle platform.

The gateways have distinct routes, identities, contracts, decisions, data, and receipts. A component cannot bypass either gateway through direct network access.

### 4.11 Database and storage exposure

Component databases, queues, object stores, internal files, and administrative storage interfaces are not public APIs.

They bind only to the minimum required interface and identity scope. Cross-component use occurs through declared application contracts rather than direct storage connections.

A shared database engine can host isolated databases or schemas. The network policy does not permit unrestricted access between those identities.

### 4.12 Outbound communication

Outbound traffic is controlled by destination and capability.

A component declares required external destinations, protocols, data classes, and failure behavior. General-purpose unrestricted outbound access is not part of the baseline.

DNS, time, package, update, registry, federation, backup, and external-service traffic remain separately identifiable.

### 4.13 Name resolution and time

Local correctness does not depend on public DNS.

Profiles provide local service discovery or stable local names where needed. A DNS result does not establish trust.

Network time can support certificate and expiry validation. When time is unavailable or uncertain, time-sensitive trust, consent, release, and publication operations enter a visible blocked state rather than using an unbounded assumption.

### 4.14 Encryption in transit

Sensitive or cross-host communication uses authenticated encryption.

Local transports can rely on operating-system protections where the applicable profile and threat model approve them.

Encryption protects transport confidentiality and integrity. It does not replace application authorization, data minimization, or acceptance validation.

### 4.15 Development network boundaries

Each development workspace receives a network namespace or equivalent logical isolation.

Fixed internal ports are permitted inside isolated workspace networks. Host ports are allocated per workspace and collision-checked.

Development services do not bind publicly by default. Production credentials and production user data are excluded from the development network baseline.

### 4.16 Offline behavior

Internet, upstream control plane, public DNS, external AI, and remote federation are not required for minimum local operation.

When a remote route is unavailable:

- local services continue where their authority is locally valid;
- eligible outbound work can be queued;
- queued work remains unexecuted;
- reconnection triggers identity, trust, consent, destination, version, time, and conflict revalidation;
- no operation is released merely because connectivity returned.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-SEC-NET-001,REQ-SEC-NET-002,REQ-SEC-NET-003,REQ-SEC-NET-004,REQ-SEC-NET-005,REQ-SEC-NET-006,REQ-SEC-NET-007,REQ-SEC-NET-008,REQ-SEC-NET-009,REQ-SEC-NET-010,REQ-SEC-NET-011,REQ-SEC-NET-012,REQ-SEC-NET-013,REQ-SEC-NET-014,REQ-SEC-NET-015,REQ-SEC-NET-016,REQ-SEC-NET-017,REQ-SEC-NET-018,REQ-SEC-NET-019,REQ-SEC-NET-020,REQ-SEC-NET-021,REQ-SEC-NET-022,REQ-SEC-NET-023,REQ-SEC-NET-024,REQ-SEC-NET-025,REQ-SEC-NET-026,REQ-SEC-NET-027,REQ-SEC-NET-028,REQ-SEC-NET-029,REQ-SEC-NET-030 -->
- **REQ-SEC-NET-001 — SHALL:** Every active network route identify source identity, destination identity, source zone, destination zone, operation class, transport, scope, payload contract, lifecycle, and failure behavior.
- **REQ-SEC-NET-002 — SHALL:** Inbound and outbound communication be denied unless an active contract explicitly permits it.
- **REQ-SEC-NET-003 — SHALL NOT:** Loopback, host co-location, container membership, cluster namespace, private addressing, LAN location, VPN presence, or successful transport authentication be treated as sufficient application authorization.
- **REQ-SEC-NET-004 — SHALL:** Every receiving component independently validate identity, authorization, tenant or authority domain, operation, purpose, payload, contract version, and applicable consent.
- **REQ-SEC-NET-005 — SHALL:** Public, private, governance, administration, federation, backup, development, external-integration, and quarantine traffic remain logically distinguishable where those zones are active.
- **REQ-SEC-NET-006 — SHALL NOT:** Public-facing services directly access private component databases, internal files, administrative sockets, or unrestricted governance state.
- **REQ-SEC-NET-007 — SHALL:** Cross-zone data movement use a versioned component interface, declared event contract, governed gateway, verified artifact, or explicit migration contract.
- **REQ-SEC-NET-008 — SHALL NOT:** A component use direct network access to write another component’s authoritative storage.
- **REQ-SEC-NET-009 — SHALL:** Administrative interfaces remain separate from public and application interfaces and use strong authentication, narrow authorization, bounded operations, rate limits, and audit evidence.
- **REQ-SEC-NET-010 — SHALL NOT:** A privileged network or local interface expose an arbitrary shell, unrestricted command forwarding, or unbounded host-operation parameters.
- **REQ-SEC-NET-011 — SHALL:** Sensitive cross-host communication use authenticated encryption and validated peer identity.
- **REQ-SEC-NET-012 — SHALL NOT:** Transport encryption, a valid certificate, or a recognized signature replace application authorization, trust-scope evaluation, consent, or destination acceptance.
- **REQ-SEC-NET-013 — SHALL:** Federation remain disabled until peer identity, trust scopes, tenant, environment, release-channel, artifact-class, capability, and authority bindings are explicit.
- **REQ-SEC-NET-014 — SHALL:** Untrusted or not-yet-accepted federation and import traffic enter a validation or quarantine boundary before authoritative use.
- **REQ-SEC-NET-015 — SHALL:** External egress identify the provider, destination, purpose, minimized data, classification, authority, retention, reuse, return path, and failure behavior.
- **REQ-SEC-NET-016 — SHALL NOT:** Components have unrestricted external egress by default or silently select a substitute external provider.
- **REQ-SEC-NET-017 — SHALL:** External AI and creative-service communication be explicit, user- or workflow-triggered as authorized, attributable, and non-authoritative until component acceptance.
- **REQ-SEC-NET-018 — SHALL:** Publication Gateway mediate governed cross-domain publication.
- **REQ-SEC-NET-019 — SHALL:** kOA Mediatheque mediate controlled local media admission, and Publication Gateway with the UCKK adapter mediate controlled outbound publication to UCKK.
- **REQ-SEC-NET-020 — SHALL NOT:** Publication Gateway, kOA Mediatheque admission, or the UCKK adapter substitute for one another or be bypassed through direct networking or direct Moodle database access.
- **REQ-SEC-NET-021 — SHALL:** Component databases, queues, object stores, internal files, and storage administration interfaces bind only to the minimum required identities and network scopes.
- **REQ-SEC-NET-022 — SHALL:** Every development workspace have a separate network namespace or equivalent isolation and collision-checked host-port allocation.
- **REQ-SEC-NET-023 — SHALL NOT:** Development services bind to public interfaces by default or receive production credentials or production user data by default.
- **REQ-SEC-NET-024 — SHALL:** Local service discovery and offline operation remain possible without public DNS, an upstream control plane, or Internet access.
- **REQ-SEC-NET-025 — SHALL:** Time-sensitive trust, consent, release, and publication operations fail closed when trusted time is unavailable or materially uncertain.
- **REQ-SEC-NET-026 — SHALL:** Queued network operations be bounded, durable where required, cancellable, and revalidated before release after reconnection.
- **REQ-SEC-NET-027 — SHALL NOT:** Reconnection, route restoration, DNS recovery, or peer availability automatically authorize queued transmission, publication, import, or activation.
- **REQ-SEC-NET-028 — SHALL:** Network observations expose route health, denials, authentication failures, authorization failures, queue state, retry state, and degraded capability without logging secrets or unnecessary protected content.
- **REQ-SEC-NET-029 — SHALL:** Removal of an integration, peer, route, component, or profile revoke related credentials and routes while preserving unrelated local capabilities and authoritative data.
- **REQ-SEC-NET-030 — SHALL NOT:** A profile, recipe, container runtime, orchestration platform, service mesh, generated context, or implementation convenience silently weaken these network boundaries.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Route registration

A route is registered through:

1. Identify the required capability.
2. Identify the source and destination components or services.
3. Identify their logical zones.
4. Identify the operation and direction.
5. Define the payload or artifact contract.
6. Define identity and authentication.
7. Define authorization, tenant, authority domain, consent, and purpose.
8. Define transport encryption and peer validation.
9. Define egress or ingress destinations.
10. Define timeouts, retries, queueing, expiry, and cancellation.
11. Define offline and reconnection behavior.
12. Define observability and evidence.
13. Register the integration.
14. Update component and profile contracts.
15. validate the route;
16. activate only after the complete validation passes.

### 6.2 Connection establishment

The connection flow is:

`text
route_resolved
 -> network_policy_checked
 -> transport_authenticated
 -> application_identity_validated
 -> authorization_validated
 -> contract_negotiated
 -> request_accepted | denied | blocked
 -> operation_executed
 -> receipt_or_response_recorded
`

A transport connection that fails application validation closes or remains restricted without executing the operation.

### 6.3 Public exposure

A public endpoint is exposed through:

1. Identify the public capability.
2. Minimize the exposed interface.
3. Confirm that the destination component owns the public state.
4. remove direct private-storage dependencies;
5. Apply authentication where the audience requires it.
6. Apply request-size, rate, concurrency, and timeout limits.
7. Apply content and payload validation.
8. Configure public-to-private denial rules.
9. Configure logging without protected content.
10. Test denial, overload, and dependency failure.
11. Publish the endpoint through the active profile mechanism.

### 6.4 Administrative access

Administrative access proceeds through:

1. Resolve the administrator identity.
2. Resolve the exact role and operation.
3. Establish the approved access path.
4. Validate device, session, and time conditions where required.
5. Open a bounded session.
6. Execute only allowlisted operations.
7. Record the action and result.
8. Close or expire the session.
9. Revoke temporary credentials.
10. Preserve evidence for review.

### 6.5 Federation peer activation

Peer activation proceeds through:

1. Exchange peer identity and capability manifests.
2. Validate trust roots and revocation state.
3. Configure tenant, environment, channel, artifact, capability, and authority scopes.
4. Configure allowed directions and data classes.
5. Configure bandwidth, priority, retry, expiry, and quarantine.
6. Test denial outside the declared scopes.
7. Test interruption and replay.
8. Record peer activation evidence.
9. Enable only the declared routes.

### 6.6 External integration activation

An external integration is activated through:

1. Resolve the active integration manifest.
2. Identify the external provider and endpoint.
3. Review data movement and classification.
4. Resolve authority and consent.
5. Configure destination-specific egress.
6. Configure minimized payload and response limits.
7. Configure credential references.
8. Configure retention, reuse, deletion, and termination behavior.
9. Test provider failure and removal.
10. Activate the bounded capability.

### 6.7 Offline transition

When a remote dependency becomes unavailable:

1. Mark the affected route unavailable.
2. Keep local routes active where authority remains valid.
3. Stop new remote transmissions.
4. Queue only operations whose contracts permit queueing.
5. Record source, destination, identity, authority, payload, version, and expiry.
6. Preserve cancellation.
7. Expose degraded state.
8. avoid substitute routes or providers;
9. Continue unrelated local operation.

### 6.8 Reconnection transition

After connectivity returns:

1. Confirm stable route availability.
2. Refresh identity and credential state.
3. Refresh trust and revocation state.
4. Refresh consent and governance decisions.
5. Revalidate destination and integration contracts.
6. Revalidate source and payload versions.
7. Revalidate time and expiry.
8. detect conflicts and partial remote effects;
9. Release only operations that still pass.
10. Retain, cancel, or replace invalid work.
11. Record transmission and destination receipts.

### 6.9 Route removal

Route removal proceeds through:

1. Stop new traffic.
2. Drain, cancel, or quarantine queued work.
3. Resolve in-flight requests.
4. Revoke credentials and trust scopes.
5. Remove firewall, proxy, route, service-discovery, and subscription entries.
6. Preserve required receipts and evidence.
7. Remove non-authoritative caches.
8. Preserve component-owned authoritative data.
9. Test unrelated local capability.
10. Record completion and external limitations.

## 7. Failure States and Safe Degradation

| Failure condition | Required behavior | Preserved capability | Denied capability |
| --- | --- | --- | --- |
| Undeclared route | Deny and record the attempted route. | Existing declared communication | Undeclared communication |
| Transport authentication fails | Close the connection. | Service availability | Requested connection |
| Application identity invalid | Reject before operation execution. | Unrelated requests | Invalid request |
| Authorization missing | Deny or block according to authority state. | Safe unrelated functions | Protected operation |
| Public endpoint overloaded | Apply rate, size, concurrency, and timeout limits. | Bounded accepted traffic | Excess traffic |
| Private database exposed publicly | Disable the exposure and fail conformance. | Component recovery | Direct public database access |
| Governance zone unavailable | Block new governed decisions. | Existing safe local reads where permitted | New governed action |
| Administration route unavailable | Preserve application service and use recovery path. | Normal application traffic | Remote administration |
| Federation peer unavailable | Queue eligible traffic without automatic release. | Local operation | Peer synchronization |
| Peer trust revoked | Disable peer routes and quarantine pending input. | Other peers and local data | Revoked peer traffic |
| External provider unavailable | Disable that capability only. | Native local capability | External integration |
| External response invalid | Quarantine or reject it. | Existing authoritative data | Candidate acceptance |
| Publication Gateway unavailable | Keep publication unexecuted. | Source storage and editing | Cross-domain publication |
| kOA Mediatheque admission unavailable | Preserve existing local media. | Read, export, backup | New local admission |
| External UCKK unavailable | Preserve local media and queued publication intent. | Local read, export, backup | Remote delivery |
| DNS unavailable | Use declared local resolution and mark remote names unavailable. | Local services | Unresolved remote route |
| Trusted time unavailable | Block time-sensitive authority. | Non-time-sensitive local functions | Expiry-sensitive operation |
| Certificate expires | Reject new sessions and expose repair state. | Existing unrelated routes | Invalid certificate route |
| Queue full | Apply backpressure and reject new queued work. | Accepted bounded queue | Additional queueing |
| Reconnection changes authority | Keep request blocked or cancelled. | Local data and evidence | Automatic release |
| Partial remote effect | Enter remediation and prevent blind retry. | Recorded state | False success |
| Observation sink unavailable | Continue bounded local security logging. | Network enforcement | Remote telemetry |
| Firewall or policy update fails | Preserve the last valid active policy. | Existing validated routes | Candidate policy |
| One zone fails | Isolate the failure. | Unrelated zones | Affected zone |
| Integration removed | Revoke its routes and credentials. | Other capabilities | Removed integration |

Safe degradation restricts communication. It does not open broad fallback routes, disable authentication, reuse another provider silently, expose private storage, or convert network availability into authority.

## 8. Cross-Component Interactions

### 8.1 Konnaxion and Orgo

Konnaxion exposes controlled public-domain interfaces. Orgo retains private workflow and operational state.

A public representation of Orgo data crosses through an explicit component contract and Publication Gateway where the disclosure domain changes. Konnaxion does not access Orgo storage directly.

### 8.2 Publication Gateway

Source components send bounded publication requests to Publication Gateway.

Publication Gateway resolves identity, trust, consent, policy, audience, destination, and representation. It sends only the approved representation to the declared destination and records a receipt.

### 8.3 kOA Mediatheque admission and external UCKK publication

User-selected media enters the kOA Mediatheque through its local admission boundary. Only separately selected and authorized media is published to online UCKK through Publication Gateway and the publication adapter. Selected UCKK learning packages return through a separate allowlisted import path into quarantine and cannot reach the local catalog directly.

The admission route is distinct from publication routes and from external creative-service routes.

### 8.4 Identity and Trust

Identity and Trust provides identity, delegation, trust, and revocation results through narrow authenticated interfaces.

Consumers validate the returned scope and expiry. They do not query identity databases directly.

### 8.5 Governance Policy Runtime

Components send the minimum policy context necessary for a decision.

Governance Policy Runtime returns a decision and obligations. It does not gain unrestricted network access to component business data.

### 8.6 Audit Broker

Components send bounded audit events or evidence references.

Audit Broker supports selective disclosure. Network logging does not become a path for unrestricted content replication.

### 8.7 Resource Governor

Resource Governor can control network egress, connection counts, queue depth, and service activation.

It does not decide whether the communication is authorized by policy or consent.

### 8.8 kOA Node Agent

kOA Node Agent exposes narrow host-lifecycle and health interfaces, preferably over node-local protected transports.

Application components do not receive general host administration access through the agent.

### 8.9 Developer workspaces

Each workspace receives separate service names, local networks or equivalent isolation, databases, ports, secrets, and process identities.

A workspace can communicate with another only through a declared test or component interface.

### 8.10 External AI and SenTient

External AI routes are explicit external integrations.

SenTient is a local optional component with isolated network access. Neither external AI nor SenTient can write component-authoritative data directly.

## 9. Decision Closure and Prohibited Assumptions

The accepted decisions referenced in the metadata close the global network-boundary model.

The following assumptions are prohibited:

1. An internal address is trusted.
2. Loopback traffic is authorized.
3. Components in one process share authority.
4. Components on one host can access each other’s databases.
5. Containers provide complete security automatically.
6. A Kubernetes namespace is an authorization boundary by itself.
7. A VPN grants application permission.
8. A valid certificate grants every operation.
9. A valid signature authorizes import or federation.
10. Public and private interfaces can share unrestricted storage access.
11. Administrators automatically possess application or cultural authority.
12. A service mesh replaces component authorization.
13. Encryption replaces data minimization.
14. General outbound HTTPS is sufficiently narrow.
15. DNS success proves destination trust.
16. Public DNS is required for local correctness.
17. Network time is always available and correct.
18. Federation is safe when a peer is reachable.
19. Reconnection authorizes queued transmission.
20. A queued request remains valid indefinitely.
21. Publication can bypass Publication Gateway on a trusted LAN.
22. Local media admission can bypass the kOA Mediatheque boundary or UCKK publication can bypass Publication Gateway.
23. Publication Gateway, local Mediatheque admission, and the UCKK adapter can share or substitute authority routes.
24. External AI is a native network dependency.
25. An unavailable external provider can be replaced silently.
26. Development services can bind publicly because the host is personal.
27. A shared database engine permits unrestricted network access.
28. Network observability requires logging payloads or secrets.
29. A profile can omit default-deny controls without explicit authority.
30. A recipe, orchestrator, runtime, or generated context can weaken the active policy.

When route identity, destination, authority, trust, consent, time, contract version, or data classification is ambiguous, the route remains blocked.

## 10. Validation Criteria

This document is conformant when:

1. It is registered as `DOC-SEC-008`.
2. Its path is `07-security/08-network-boundaries.md`.
3. Its class is `normative_markdown`.
4. Its status is `active`.
5. Its language is `en`.
6. Its layer is `security`.
7. Its scope is `global`.
8. Its metadata matches `generated/document-index.json`.
9. Every canonical reference resolves.
10. Every listed decision resolves with accepted status.
11. Every listed requirement resolves and matches the generated block.
12. Every listed lock resolves and passes.
13. The eleven mandatory sections exist in the required order.
14. Normative keywords occur only in the generated requirements block.
15. Every active route resolves to an active integration or profile contract.
16. Unregistered inbound and outbound routes are denied.
17. Public-to-private direct storage access tests fail as expected.
18. Component-to-component direct authoritative-storage writes fail.
19. Cross-zone requests validate identity, scope, contract, and policy.
20. Administrative interfaces are separate and audited.
21. Privileged interfaces reject arbitrary operations and parameters.
22. Federation routes remain disabled without explicit peer scopes.
23. External egress is destination-specific and data-minimized.
24. Local Mediatheque admission and UCKK publication-boundary separation tests pass.
25. Development workspaces have isolated networks or equivalent controls and unique host ports.
26. Public DNS and Internet loss do not break minimum local operation.
27. Time uncertainty blocks time-sensitive authority.
28. Queued traffic does not release automatically after reconnection.
29. Removed integrations lose credentials and routes.
30. Observability excludes secrets and unnecessary protected content.
31. Profile-specific network mechanisms preserve equivalent authority semantics.
32. Kubernetes, containers, and service meshes remain optional unless a profile explicitly adopts them.
33. Traceability and active evidence are complete.
34. No unresolved marker, provisional value, parallel authority, or file-content hash requirement appears.
35. Complete documentation validation returns `pass`.

## 11. Non-Normative Examples

### 11.1 Sovereign hub zones

A sovereign hub exposes Konnaxion through the public zone, runs Orgo in the private zone, places identity and policy services in the governance zone, restricts administration to a dedicated path, configures federation per peer, and sends backups through a separate target route.

### 11.2 Lightweight endpoint

A lightweight endpoint implements the zones as local service policies on one Linux host. The interface can use loopback, but every component call still carries identity and operation scope.

### 11.3 Development worktrees

Two Konnaxion worktrees use fixed internal port `8080` inside separate rootless container networks. Their host ports differ and are recorded by workspace identity.

### 11.4 External translation

A user explicitly requests external translation. The responsible component opens egress only to the approved provider, sends the bounded text, records the transfer, and receives candidate output through controlled import.

### 11.5 Federation revocation

A peer trust scope is revoked. The hub disables the peer route, stops new synchronization, quarantines pending inbound artifacts, preserves local data, and records the revocation.

### 11.6 DNS outage

Public DNS becomes unavailable. Local service discovery, private workflows, Kristal access, local publication between authorized domains, administration, and backup to a local target continue.

### 11.7 Time uncertainty

The host clock becomes uncertain after a long offline interval. Non-sensitive local reads continue, but certificate renewal, expiring consent, trust, federation, and publication operations remain blocked.

### 11.8 Public service compromise attempt

A public Konnaxion process attempts to connect directly to an Orgo database. Network policy denies the route, and component-boundary validation records the attempt.

### 11.9 Administrative maintenance

An operator authenticates through the administration boundary and invokes a narrow node-health operation. The operator does not receive access to application data or a general shell through the application route.

### 11.10 Reconnection

A queued federation export remains pending after the peer returns. Trust, revocation, source version, destination capability, and conflict state are revalidated before transmission.
