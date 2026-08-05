<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SEC-000",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "security",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "01-constitution/04-explicit-authority.md",
    "02-system/01-system-context.md",
    "02-system/11-ariane-system-boundary.md",
    "02-system/19-release-and-artifact-identity.md",
    "03-profiles/11-high-assurance.md",
    "04-components/subsystems/semantik-architect.md",
    "04-components/publication-gateway.md",
    "05-development/05-python-uv.md",
    "05-development/15-artifact-publication.md",
    "06-lifecycle/08-kristal-artifacts.md",
    "06-lifecycle/18-sbom-provenance-and-signing.md",
    "generated/component-catalog.json",
    "generated/test-catalog.json",
    "contracts/profiles/high-assurance.profile.json",
    "contracts/artifact-contracts/sovereignty-bundle.schema.json",
    "schemas/component-contract.schema.json"
  ],
  "decision_ids": [
    "DEC-AUTH-001",
    "DEC-IDENT-001",
    "DEC-DATA-001",
    "DEC-COMP-001",
    "DEC-GOV-001",
    "DEC-PRIV-001",
    "DEC-AI-001",
    "DEC-LIFE-001",
    "DEC-GATE-001",
    "DEC-SENT-001",
    "DEC-MEDIATHEQUE-001",
    "DEC-UCKK-EXT-001",
    "DEC-ARI-001",
    "DEC-LANG-001",
    "DEC-KRISTAL-001",
    "DEC-HW-001"
  ],
  "requirement_ids": [
    "REQ-SEC-THREAT-001",
    "REQ-SEC-THREAT-002",
    "REQ-SEC-THREAT-003",
    "REQ-SEC-THREAT-004",
    "REQ-SEC-THREAT-005",
    "REQ-SEC-THREAT-006",
    "REQ-SEC-THREAT-007",
    "REQ-SEC-THREAT-008",
    "REQ-SEC-THREAT-009",
    "REQ-SEC-THREAT-010",
    "REQ-SEC-THREAT-011",
    "REQ-SEC-THREAT-012",
    "REQ-SEC-THREAT-013",
    "REQ-SEC-THREAT-014",
    "REQ-SEC-THREAT-015",
    "REQ-SEC-THREAT-016",
    "REQ-SEC-THREAT-017",
    "REQ-SEC-THREAT-018",
    "REQ-SEC-THREAT-019",
    "REQ-SEC-THREAT-020",
    "REQ-SEC-THREAT-021",
    "REQ-SEC-THREAT-022",
    "REQ-SEC-THREAT-023",
    "REQ-SEC-THREAT-024",
    "REQ-SEC-THREAT-025",
    "REQ-SEC-THREAT-026",
    "REQ-SEC-THREAT-027",
    "REQ-SEC-THREAT-028",
    "REQ-SEC-THREAT-029",
    "REQ-SEC-THREAT-030",
    "REQ-SEC-THREAT-031",
    "REQ-SEC-THREAT-032",
    "REQ-SEC-THREAT-033",
    "REQ-SEC-THREAT-034",
    "REQ-SEC-THREAT-035",
    "REQ-SEC-THREAT-036",
    "REQ-SEC-THREAT-037",
    "REQ-SEC-THREAT-038",
    "REQ-SEC-THREAT-039",
    "REQ-SEC-THREAT-040",
    "REQ-SEC-THREAT-041",
    "REQ-SEC-THREAT-042",
    "REQ-SEC-THREAT-043",
    "REQ-SEC-THREAT-044"
  ],
  "lock_ids": [
    "LOCK-AUTH-001",
    "LOCK-AUTH-002",
    "LOCK-AUTH-003",
    "LOCK-AUTH-004",
    "LOCK-IDENT-001",
    "LOCK-DATA-001",
    "LOCK-COMP-001",
    "LOCK-GOV-001",
    "LOCK-PRIV-001",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-GATE-001",
    "LOCK-SENT-001",
    "LOCK-ARI-001",
    "LOCK-MEDIATHEQUE-001",
    "LOCK-MEDIATHEQUE-002",
    "LOCK-UCKK-EXT-001",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-UCKK-EXT-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-004",
    "DOC-SYS-001",
    "DOC-SYS-011",
    "DOC-SYS-019",
    "DOC-PROF-011",
    "DOC-COMP-PUBGATE",
    "DOC-DEV-005",
    "DOC-DEV-015",
    "DOC-LIFE-008",
    "DOC-LIFE-018"
  ],
  "tags": [
    "threat-model",
    "security",
    "trust-boundaries",
    "authority",
    "privacy",
    "supply-chain",
    "offline",
    "recovery",
    "ai-boundaries",
    "cultural-rights",
    "denial-of-service",
    "exit"
  ]
}
KOA:DOC-META:END -->

# Threat Model

## 1. Purpose

This document defines the global kOA threat model.

It identifies:

- protected assets;
- adversary classes;
- trust-boundary classes;
- attack and abuse scenarios;
- system-wide security objectives;
- control ownership;
- failure and degradation expectations;
- residual risk;
- validation and evidence requirements.

This document owns the global threat identifiers and shared threat framing.

Detailed controls remain owned by the applicable:

- constitution;
- system documents;
- profiles;
- component contracts;
- artifact contracts;
- lifecycle documents;
- development documents;
- operations procedures;
- test and evidence registries.

The security model treats fabricated authority, silent cross-domain mutation, irreversible capture, and loss of credible exit as security failures alongside conventional confidentiality, integrity, and availability failures.

## 2. Scope

The threat model covers:

- endpoints, sovereign nodes, hubs, build farms, and control planes;
- human, service, workload, node, publisher, signer, artifact, tenant, and authority identities;
- Konnaxion, Orgo, Kristal, the kOA Mediatheque, Ariane, SemantiK, GF Wordbench, SenTient, gateways, governance, identity, audit, resource, and node-control components, plus external integrations such as UCKK;
- public, private, tenant, community, evidence, build, signing, and recovery domains;
- online, offline, removable-media, federation, mirror, backup, export, and restore paths;
- system, services, governance, and knowledge release channels;
- optional external AI and integration surfaces;
- institutional, semantic, cultural, and governance capture;
- accidental misuse and operational failure.

It does not claim to prove:

- legitimate governance;
- factual truth;
- correct cultural authority;
- freedom from physical coercion;
- immunity from every unknown vulnerability;
- universal agreement about semantics or public value.

The model applies throughout design, implementation, testing, deployment, operation, incident response, recovery, migration, and exit.

## 3. Canonical References

| Canonical reference | Security ownership |
| --- | --- |
| `01-constitution/04-explicit-authority.md` | Explicit authority, non-fabrication, separation, fail-closed behavior, and recourse. |
| `02-system/01-system-context.md` | Global component boundaries, external actors, offline baseline, data domains, and trust context. |
| `02-system/11-ariane-system-boundary.md` | Guidance, automation, sensitive confirmation, voice candidate boundaries, and user control. |
| `02-system/19-release-and-artifact-identity.md` | Artifact identity, independent release channels, verification, activation, rollback, revocation, and evidence. |
| `03-profiles/11-high-assurance.md` | Hardware trust, measured or verified boot, attestation, key custody, separation of duties, and high-assurance evidence. |
| `04-components/publication-gateway.md` | Private-to-public disclosure, redaction, approval, publication receipts, withdrawal, and supersession. |
| `04-components/gf-wordbench.md` | Deterministic language construction and separation from SemantiK runtime activation. |
| `05-development/05-python-uv.md` | Development-workspace dependency isolation and separation from service-state isolation. |
| `05-development/15-artifact-publication.md` | Builder, verifier, signer, publisher, release, and activation separation. |
| `06-lifecycle/08-kristal-artifacts.md` | Epistemic status, audience, query, offline trust, activation, and revocation lifecycle. |
| `06-lifecycle/18-sbom-provenance-and-signing.md` | Supply-chain evidence, signing scope, key lifecycle, trust roots, and offline verification. |
| `generated/component-catalog.json` | Component identities, authoritative data ownership, global boundaries, and relationships. |
| `contracts/profiles/high-assurance.profile.json` | Machine-readable high-assurance control envelope. |
| `contracts/artifact-contracts/sovereignty-bundle.schema.json` | Complete export, trust handover, clean restore, rights, evidence, and independent exit. |
| `generated/test-catalog.json` | Security, boundary, lifecycle, profile, operations, and exit test definitions. |
| `schemas/component-contract.schema.json` | Required component security, privilege, failure, data, interface, and conformance fields. |

## 4. Model and Responsibilities

### 4.1 Security objectives

The architecture prioritizes these objectives in order of safety relevance rather than as an absolute performance order:

1. prevent fabrication or silent expansion of authority;
2. protect human safety, due process, consent, and recourse;
3. contain compromise within tenant, component, profile, and capability boundaries;
4. preserve confidentiality of private, sensitive, restricted, secret, and culturally governed data;
5. preserve integrity, identity, provenance, and status;
6. retain minimum local availability and last-known-good operation;
7. maintain classified evidence without creating a surveillance system;
8. support rollback, recovery, portability, institutional memory, and credible exit;
9. keep optional integrations and AI removable;
10. expose disagreement, uncertainty, degradation, and stale trust rather than hiding them.

### 4.2 Protected assets

| Asset ID | Protected asset | Security meaning | Criticality |
| --- | --- | --- | --- |
| `ASSET-SEC-001` | Human safety and due process | Safety, procedural fairness, appeal, consent, and protection from fabricated authority. | critical |
| `ASSET-SEC-002` | Authority and governance | Policy identity, delegation, approvals, emergency authority, dissent, recourse, and history. | critical |
| `ASSET-SEC-003` | Identity and credentials | Human, role, organization, tenant, node, workload, publisher, signer, and artifact identities. | critical |
| `ASSET-SEC-004` | Private operational state | Orgo cases, evidence, tasks, decisions, protected communications, and restricted workflows. | critical |
| `ASSET-SEC-005` | Public accountability state | Konnaxion public records, participation, discovery, decision integrity, and public receipts. | high |
| `ASSET-SEC-006` | Epistemic integrity | Kristal content, provenance, validation, recognition, status, lineage, query contracts, and Runtime Packs. | critical |
| `ASSET-SEC-007` | Media and cultural material | kOA Mediatheque originals, transformations, identities, rights, consent, audience, attribution, and withdrawal state; UCKK publication packages and receipts where applicable. | critical |
| `ASSET-SEC-008` | Language and navigation artifacts | Compiled language packs, SemantiK runtime state, Ariane Atlases, drivers, and deterministic guidance. | high |
| `ASSET-SEC-009` | Release and supply-chain integrity | Source identity, toolchains, artifacts, SBOMs, provenance, signatures, releases, Release Sets, and revocations. | critical |
| `ASSET-SEC-010` | Keys and trust roots | Signing, authority, node, workload, encryption, audit, recovery, and trust-delegation material. | critical |
| `ASSET-SEC-011` | Audit and evidence | Security, governance, publication, activation, recovery, and access evidence. | critical |
| `ASSET-SEC-012` | Availability and recovery | Minimum local operation, last-known-good artifacts, backups, restore procedures, capacity, and incident response. | critical |
| `ASSET-SEC-013` | Sovereignty and exit | Portable exports, independent verification, clean restore, institutional memory, and removal of integrations. | critical |

### 4.3 Adversary classes

| Adversary ID | Adversary | Typical capability or objective |
| --- | --- | --- |
| `ADV-SEC-001` | Remote unauthenticated attacker | Exploit public endpoints, parsers, authentication, network services, or exposed management surfaces. |
| `ADV-SEC-002` | Malicious or compromised participant | Abuse valid user capabilities, content submission, voting, reporting, discovery, or workflow access. |
| `ADV-SEC-003` | Malicious tenant or organization administrator | Cross tenant boundaries, grant excessive roles, suppress evidence, or manipulate local policy. |
| `ADV-SEC-004` | Compromised public or private service | Move laterally, forge events, read protected state, or perform unauthorized writes. |
| `ADV-SEC-005` | Privileged host or infrastructure operator | Bypass normal governance, alter files, replace trust, extract secrets, or suppress evidence. |
| `ADV-SEC-006` | Supply-chain or repository attacker | Substitute source, dependencies, build tools, artifacts, signatures, manifests, or revocation state. |
| `ADV-SEC-007` | Malicious integration or external provider | Exfiltrate data, return deceptive state, create lock-in, or become an undocumented authority. |
| `ADV-SEC-008` | Physical attacker | Steal a node, inspect storage, alter boot media, attach malicious devices, or tamper with removable media. |
| `ADV-SEC-009` | Federation or peer adversary | Replay stale records, claim deceptive authority, inject conflicting identifiers, or amplify abusive traffic. |
| `ADV-SEC-010` | AI or automated tool with unsafe output | Produce confident falsehoods, hidden transformations, sensitive-data leakage, or unauthorized action suggestions. |
| `ADV-SEC-011` | Governance or semantic insider | Change rules, definitions, rankings, translations, recognition, or emergency powers gradually and legitimately enough to evade simple anomaly checks. |
| `ADV-SEC-012` | Resource-exhaustion attacker | Create retry storms, queue growth, parser bombs, storage pressure, expensive queries, or synchronization floods. |
| `ADV-SEC-013` | Recovery or exit adversary | Use backup, export, restore, break-glass, migration, or key handover to seize authority or extract data. |
| `ADV-SEC-014` | Accidental authorized actor | Cause security impact through misconfiguration, mistaken publication, unsafe recovery, incorrect scope, or misunderstood status. |

The adversary model includes actors with valid credentials and actors operating through legitimate governance procedures. Security review does not limit itself to unauthenticated remote attackers.

### 4.4 Trust boundaries

| Boundary ID | Boundary | Control purpose | Required control themes |
| --- | --- | --- | --- |
| `TB-SEC-001` | Human or client to service | Required control themes | Authentication, session, tenant, request validation, rate limits, anti-automation, and capability authorization. |
| `TB-SEC-002` | Public Konnaxion to private Orgo | Required control themes | Explicit intake, classification, provenance, rate limits, anti-Sybil controls, and no shared persistence. |
| `TB-SEC-003` | Private Orgo to public Konnaxion | Required control themes | Publication Gateway, minimization, redaction, approval, durable receiving receipt, withdrawal, and supersession. |
| `TB-SEC-004` | Component to component | Required control themes | Versioned interfaces, service identity, authorization, idempotency, bounded retries, event integrity, and direct-write prohibition. |
| `TB-SEC-005` | Service to host privilege | Required control themes | kOA Node Agent allowlist, schema binding, policy decision binding, replay protection, receipts, and no arbitrary shell. |
| `TB-SEC-006` | Build to signing | Required control themes | Fixed candidate identity, verification, approval, protected key custody, separation of duties, and signed-statement scope. |
| `TB-SEC-007` | Repository or mirror to runtime | Required control themes | Quarantine, inventory, signatures, trust roots, revocation, downgrade protection, compatibility, staging, and independent activation. |
| `TB-SEC-008` | Removable media to node | Required control themes | Bounded parsing, no auto-execution, decompression limits, isolated staging, trust verification, and explicit import authority. |
| `TB-SEC-009` | Core to external AI or integration | Required control themes | Explicit initiation, data eligibility, destination allowlist, provenance, non-authoritative return, and removable operation. |
| `TB-SEC-010` | Federation peer to local domain | Required control themes | Peer identity, authority scope, replay protection, conflict representation, rate limits, and local admission. |
| `TB-SEC-011` | Operational state to audit evidence | Required control themes | Classification, minimization, tamper resistance, protected access, retention, and independent evidence correlation. |
| `TB-SEC-012` | Backup or sovereignty bundle to clean restore | Required control themes | Complete inventory, encryption, trust handover, independent verification, migration, index rebuild, workflow resume, and no implicit activation. |
| `TB-SEC-013` | Offline node to stale trust context | Required control themes | Known trust and revocation epoch, clock confidence, visible staleness, policy response, and emergency path. |
| `TB-SEC-014` | Profile or control plane to node realization | Required control themes | Profile-scoped topology, hardware trust, orchestration declaration, resources, network exposure, and drift evidence. |

### 4.5 Threat catalog

| Threat ID | Threat | Scenario | Primary assets | Primary controls | Residual risk |
| --- | --- | --- | --- | --- | --- |
| `THREAT-SEC-001` | Host or service compromise | Code execution is used for lateral movement, persistence, secret access, or authoritative mutation. | ASSET-SEC-003, ASSET-SEC-004, ASSET-SEC-010, ASSET-SEC-012 | Dedicated identities, rootless or constrained execution, read-only images, minimal capabilities, mandatory access control, network policy, narrow privileged broker, immutable artifacts, drift and health evidence. | A sufficiently privileged physical or infrastructure operator can still coerce or disable a node. |
| `THREAT-SEC-002` | Release supply-chain substitution | Source, dependency, build worker, registry, manifest, SBOM, provenance, signature, release, or mirror content is replaced. | ASSET-SEC-006, ASSET-SEC-008, ASSET-SEC-009, ASSET-SEC-010 | Fixed identities, lockfiles, isolated builds, verifiable SBOM and provenance, scoped signatures, immutable repositories, Release Set compatibility, revocation, downgrade protection, independent target verification. | Trusted builders, signers, or roots can be compromised before detection. |
| `THREAT-SEC-003` | Policy capture | Rules, thresholds, disclosure, emergency powers, exceptions, or approval requirements are changed to legalize abuse. | ASSET-SEC-001, ASSET-SEC-002, ASSET-SEC-004, ASSET-SEC-011 | Signed independent governance releases, semantic diff, simulation, multi-party approval, expiry, receipts, public policy identity, recourse, fork and exit. | Legitimate authorities can approve harmful policy; technical controls expose but do not resolve legitimacy. |
| `THREAT-SEC-004` | Semantic or translation capture | Definitions, ontologies, translations, authority defaults, reader policies, or language artifacts alter meaning deceptively. | ASSET-SEC-006, ASSET-SEC-008 | Versioned artifacts, source lineage, contested states, scoped recognition, deterministic compilation and rendering, multiple readings, independent activation, rollback, local forkability. | Meaning remains socially contested and cannot be proven correct by software alone. |
| `THREAT-SEC-005` | Ranking and visibility capture | Brigading, reputation laundering, hidden weighting, Sybil identities, or opaque advisory logic controls discovery. | ASSET-SEC-001, ASSET-SEC-005, ASSET-SEC-006 | Baseline and advisory separation, public policy identity, explanation, domain-bounded signals, anti-Sybil controls, rate limits, audit, appeal, and removable integrations. | Coordinated social manipulation can remain difficult to distinguish from legitimate participation. |
| `THREAT-SEC-006` | Privacy collapse through accountability | Logs, audit, public receipts, explanations, or support bundles reveal vulnerable people or restricted evidence. | ASSET-SEC-001, ASSET-SEC-004, ASSET-SEC-007, ASSET-SEC-011 | Classified evidence, minimization, selective disclosure, pseudonymous public receipts, encryption, protected access audit, retention, redaction, sanitized support bundles. | Re-identification remains possible when public contextual data is rich. |
| `THREAT-SEC-007` | Public and private domain contamination | Untrusted public input enters private or trusted state without admission, or private data leaks to public surfaces. | ASSET-SEC-004, ASSET-SEC-005, ASSET-SEC-006 | Separate components and stores, explicit intake, Publication Gateway, classification, redaction, approval, signed or identified bundles, no shared database, receiving receipts. | Authorized publication can still disclose more than intended because of human review error. |
| `THREAT-SEC-008` | AI overreach or data exfiltration | AI output becomes policy, authority, privileged action, recognition, cultural decision, or hidden data-transfer channel. | ASSET-SEC-001, ASSET-SEC-002, ASSET-SEC-004, ASSET-SEC-006, ASSET-SEC-007 | No native dependency, explicit capability policy, no-AI enforcement, data minimization, provenance, candidate status, human or community review, deterministic gates, no direct privilege or authoritative writes. | Reviewers can over-trust fluent output or fail to detect provider retention and inference risks. |
| `THREAT-SEC-009` | Offline downgrade and stale trust | A disconnected node accepts an older, revoked, expired, or insecure artifact or authority state. | ASSET-SEC-002, ASSET-SEC-006, ASSET-SEC-008, ASSET-SEC-009, ASSET-SEC-012 | Monotonic state, downgrade and substitution resistance, trusted revocation epoch, expiry, clock confidence, visible staleness, last-known-good retention, separately authorized emergency path. | An isolated node cannot know events that occurred after its latest trusted update. |
| `THREAT-SEC-010` | Malicious offline media or parser bomb | A bundle exploits archive parsing, decompression, paths, recursion, object counts, storage, or operator trust. | ASSET-SEC-009, ASSET-SEC-010, ASSET-SEC-012 | Quarantine, safe relative paths, size and recursion limits, no auto-execution, isolated staging, complete inventory, signature and trust checks, explicit policy decision. | Unknown parser vulnerabilities can remain in complex formats. |
| `THREAT-SEC-011` | Denial of service and retry storm | Expensive requests, dependency failures, floods, retries, queues, or storage growth exhaust the system. | ASSET-SEC-001, ASSET-SEC-004, ASSET-SEC-005, ASSET-SEC-012 | Timeout budgets, quotas, bounded queues, backoff and jitter, circuit breakers, bulkheads, priority work, task activation, cancellation, capability-scoped degradation, capacity evidence. | A large enough attacker or infrastructure loss can still deny service. |
| `THREAT-SEC-012` | Insider root or infrastructure abuse | A privileged operator bypasses governance, changes files, replaces trust, extracts data, or suppresses evidence. | ASSET-SEC-002, ASSET-SEC-004, ASSET-SEC-009, ASSET-SEC-010, ASSET-SEC-011 | Immutable or verified base, narrow operations, protected keys, separation of duties, measured or verified boot, attestation, receipts, drift detection, external evidence, clean exit. | Physical control and coercion can exceed software containment. |
| `THREAT-SEC-013` | Credential, delegation, and Sybil abuse | Fake, stolen, replayed, over-scoped, or laundered identities undermine access or legitimacy. | ASSET-SEC-001, ASSET-SEC-002, ASSET-SEC-003, ASSET-SEC-005 | Layered identities, scoped credentials, issuer verification, explicit delegation, revocation, replay protection, tenant binding, domain-bounded competence, contestable evidence. | Identity assurance can be weak when source institutions or social proof are compromised. |
| `THREAT-SEC-014` | Cultural extraction and rights violation | Restricted material is exposed, reused, federated, exported, or sent to AI without legitimate authority. | ASSET-SEC-001, ASSET-SEC-007, ASSET-SEC-013 | Rights objects, audience-specific artifacts, encryption, no-AI enforcement, consent and steward authority, withdrawal propagation, attribution, export restrictions, audited access. | Technical enforcement cannot settle contested authority or undo all copied disclosures. |
| `THREAT-SEC-015` | Recovery capture | Recovery, break-glass, trust replacement, backup, key handover, or restore is abused to seize authority or extract data. | ASSET-SEC-002, ASSET-SEC-004, ASSET-SEC-010, ASSET-SEC-012, ASSET-SEC-013 | Separate recovery environment, stronger authentication, expiry, dual or threshold control, protected key handling, clean restore, independent verification, explicit receipts, post-event review. | Emergency conditions can pressure operators into accepting weaker controls. |
| `THREAT-SEC-016` | Tenant or domain confusion | A request, token, event, cache, query, or background job executes under the wrong tenant, environment, audience, or authority domain. | ASSET-SEC-003, ASSET-SEC-004, ASSET-SEC-005, ASSET-SEC-006, ASSET-SEC-007 | Tenant context on every operation, scoped identities, partitioned stores, explicit audience, cache-key binding, non-leaking errors, cross-tenant tests, protected evidence. | Complex multi-tenant migrations and asynchronous processing remain error-prone. |
| `THREAT-SEC-017` | Direct cross-component mutation | A component bypasses interfaces and edits another component's authoritative data, eliminating validation and evidence. | ASSET-SEC-002, ASSET-SEC-004, ASSET-SEC-005, ASSET-SEC-006 | Canonical ownership, separate stores, database credential separation, network policy, versioned contracts, mutation receipts, schema checks, boundary tests. | Shared host administrators can still alter multiple stores outside normal interfaces. |
| `THREAT-SEC-018` | Secret or key leakage | Secrets appear in images, environment variables, logs, crash dumps, caches, source, exports, or support bundles. | ASSET-SEC-003, ASSET-SEC-010, ASSET-SEC-011, ASSET-SEC-013 | Reference-based secret delivery, minimal service access, protected custody, scanning, log filtering, export rules, rotation, revocation, sanitized diagnostics, protected handover profile. | Secrets can be exposed through memory compromise or operator screenshots. |
| `THREAT-SEC-019` | Publication and activation confusion | A published or copied artifact is treated as installed or active without independent target verification and authority. | ASSET-SEC-006, ASSET-SEC-008, ASSET-SEC-009, ASSET-SEC-012 | Separate lifecycle states, quarantine, staging, compatibility, governance decision, atomic activation, health tests, last-known-good state, activation receipts. | Operators can still misunderstand status if interfaces communicate it poorly. |
| `THREAT-SEC-020` | Federation deception or replay | A peer presents stale, conflicting, forged, replayed, or differently scoped authority and content. | ASSET-SEC-002, ASSET-SEC-005, ASSET-SEC-006, ASSET-SEC-007 | Peer and artifact identity, authority scope, monotonic sequence, replay protection, conflict representation, local admission, rate limits, revocation, provenance. | Legitimate authorities can disagree and no universal resolver exists. |
| `THREAT-SEC-021` | Evidence tampering or selective logging | An actor removes, fabricates, delays, overcollects, or selectively exposes evidence to distort accountability. | ASSET-SEC-001, ASSET-SEC-002, ASSET-SEC-011 | Transactional outbox, append-only or protected stores, classified evidence, correlation identities, local durability, independent anchors where required, access audit, retention and export. | Colluding evidence authorities can still conceal activity until external comparison. |
| `THREAT-SEC-022` | Physical theft or boot tampering | A node or storage device is stolen, modified, cold-booted, or started from altered firmware or media. | ASSET-SEC-004, ASSET-SEC-009, ASSET-SEC-010, ASSET-SEC-012 | Volume encryption, hardware-bound secrets, Secure Boot or equivalent, measured boot where declared, console protection, revocation, remote or offline recovery, attestation. | Unlocked or running devices can expose live data to a physical attacker. |
| `THREAT-SEC-023` | Integration or dependency capture | An optional tool becomes mandatory, changes semantics, monopolizes data, or prevents local correctness and exit. | ASSET-SEC-006, ASSET-SEC-009, ASSET-SEC-012, ASSET-SEC-013 | Native, annexed, connected, mimicked, or forbidden classification; anti-corruption layer; removable operation; local minimum capability; export; bounded network and data access. | Organizations can become socially dependent on a tool even when technical removal remains possible. |
| `THREAT-SEC-024` | Exit lock-in or incomplete export | The operator withholds data, omits relationships, exports unverifiable state, or makes restoration depend on itself. | ASSET-SEC-004, ASSET-SEC-006, ASSET-SEC-007, ASSET-SEC-011, ASSET-SEC-013 | Sovereignty Bundle, complete inventory, independent references, signatures, provenance, rights, trust handover, clean restore, workflow resume tests, no original-operator dependency. | Legal, physical, or institutional barriers can still prevent possession or use of an otherwise valid export. |
| `THREAT-SEC-025` | Time and freshness manipulation | Clock, expiry, sequence, revocation epoch, lease, certificate, or approval freshness is manipulated or unavailable. | ASSET-SEC-002, ASSET-SEC-003, ASSET-SEC-009, ASSET-SEC-010, ASSET-SEC-012 | Monotonic sequence where possible, bounded clock confidence, signed epochs, expiry checks, replay protection, visible uncertainty, policy response, independent evidence. | Offline environments cannot always establish trusted wall-clock time. |

### 4.6 Security control ownership

| Control domain | Canonical owner |
| --- | --- |
| Global threat IDs, assets, adversaries, boundaries, objectives, residual-risk framing | This document |
| Global explicit authority and prohibited authority fabrication | Constitution |
| Component identity, ownership, interfaces, stores, events, states, privilege, failures, and conformance | Component registry and component contracts |
| Profile membership, topology, hardware, host hardening, process isolation, networks, resources, and offline envelope | Profile contracts |
| Artifact identity, verification, signing requirements, activation, rollback, revocation, and evidence | Artifact-class and lifecycle contracts |
| System, services, governance, and knowledge release channels | Release-channel contracts |
| Identity, credentials, trust roots, delegation, and revocation | Identity and Trust contract |
| Governed decisions, obligations, exceptions, emergency authority, and expiry | Governance Policy Runtime contract |
| Narrow privileged operations | kOA Node Agent contract |
| Evidence storage and protected-evidence access | Audit Broker contract |
| Resource quotas, queues, priorities, pressure behavior, and heavy-job activation | Resource Governor contract |
| Private-to-public disclosure | Publication Gateway contract |
| Local media-ingestion boundary | kOA Mediatheque component contract |
| External UCKK publication boundary | UCKK publication integration contract |
| Recovery, backup, restore, support, and incident execution | Operations documents and applicable component contracts |
| Test definitions and executed results | Test Catalog and Evidence registries |

### 4.7 Risk evaluation

Threat reviews use qualitative impact and exposure rather than unsupported numerical precision.

Impact considers:

- human harm;
- authority fabrication;
- cross-tenant disclosure;
- persistent integrity loss;
- key or trust compromise;
- public/private contamination;
- cultural-rights violation;
- irreversible publication;
- inability to recover;
- inability to exit.

Exposure considers:

- public reachability;
- privilege level;
- data classification;
- trust scope;
- offline import;
- federation;
- persistence;
- automation;
- reversibility;
- observability.

A threat can be unacceptable even when technically rare if it fabricates authority, irreversibly discloses protected material, or destroys recovery.

### 4.8 Assumptions

The baseline assumes:

- cryptographic primitives and protected hardware used by an active profile behave within their declared assurance;
- operating-system and firmware maintenance paths exist;
- at least one authorized recovery path remains physically accessible;
- human reviewers can make mistakes and can be malicious;
- network and remote services can be unavailable;
- clocks can be inaccurate or untrusted;
- external systems can change semantics or terms;
- no single audit record is treated as infallible;
- governance can be captured through formally valid actions;
- clean exit can require legal and organizational action in addition to technical export.

These assumptions narrow claims. They do not grant authority.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-SEC-THREAT-001,REQ-SEC-THREAT-002,REQ-SEC-THREAT-003,REQ-SEC-THREAT-004,REQ-SEC-THREAT-005,REQ-SEC-THREAT-006,REQ-SEC-THREAT-007,REQ-SEC-THREAT-008,REQ-SEC-THREAT-009,REQ-SEC-THREAT-010,REQ-SEC-THREAT-011,REQ-SEC-THREAT-012,REQ-SEC-THREAT-013,REQ-SEC-THREAT-014,REQ-SEC-THREAT-015,REQ-SEC-THREAT-016,REQ-SEC-THREAT-017,REQ-SEC-THREAT-018,REQ-SEC-THREAT-019,REQ-SEC-THREAT-020,REQ-SEC-THREAT-021,REQ-SEC-THREAT-022,REQ-SEC-THREAT-023,REQ-SEC-THREAT-024,REQ-SEC-THREAT-025,REQ-SEC-THREAT-026,REQ-SEC-THREAT-027,REQ-SEC-THREAT-028,REQ-SEC-THREAT-029,REQ-SEC-THREAT-030,REQ-SEC-THREAT-031,REQ-SEC-THREAT-032,REQ-SEC-THREAT-033,REQ-SEC-THREAT-034,REQ-SEC-THREAT-035,REQ-SEC-THREAT-036,REQ-SEC-THREAT-037,REQ-SEC-THREAT-038,REQ-SEC-THREAT-039,REQ-SEC-THREAT-040,REQ-SEC-THREAT-041,REQ-SEC-THREAT-042,REQ-SEC-THREAT-043,REQ-SEC-THREAT-044 -->
- **REQ-SEC-THREAT-001 — SHALL:** This document is the canonical owner of global protected-asset classes, adversary classes, trust-boundary classes, threat identifiers, security objectives, and residual-risk framing.
- **REQ-SEC-THREAT-002 — SHALL:** Component, profile, artifact, lifecycle, development, and operations contracts own their detailed controls and do not create a second global threat catalog.
- **REQ-SEC-THREAT-003 — SHALL:** Security decisions protect human safety, due process, legitimate authority, privacy, integrity, provenance, availability, recourse, cultural rights, and credible exit.
- **REQ-SEC-THREAT-004 — SHALL:** Missing, ambiguous, stale, revoked, or unverifiable authority blocks the affected governed action.
- **REQ-SEC-THREAT-005 — SHALL:** Authentication, identity resolution, authorization, policy evaluation, signing, publication, activation, and runtime ownership remain distinct security decisions.
- **REQ-SEC-THREAT-006 — SHALL:** Tenant, environment, public, private, component, workload, and evidence domains remain explicitly separated.
- **REQ-SEC-THREAT-007 — SHALL NOT:** A component reads or writes another component's authoritative store through direct database access.
- **REQ-SEC-THREAT-008 — SHALL:** Cross-component mutation uses an authenticated, authorized, versioned, bounded, observable, and failure-defined contract.
- **REQ-SEC-THREAT-009 — SHALL:** Privileged host operations remain allowlisted, schema-bound, operation-bound, replay-protected, time-bounded, and receipted.
- **REQ-SEC-THREAT-010 — SHALL NOT:** General root execution, arbitrary privileged shell access, or unrestricted host mutation is exposed as an ordinary component interface.
- **REQ-SEC-THREAT-011 — SHALL:** Release, governance, authority, audit, recovery, node, workload, and data-encryption keys use distinct scoped identities and lifecycle controls.
- **REQ-SEC-THREAT-012 — SHALL NOT:** Protected private keys are normally exportable to developer workspaces, ordinary build workers, application processes, logs, caches, or support bundles.
- **REQ-SEC-THREAT-013 — SHALL:** Artifact verification, publication, release, staging, activation, rollback, revocation, and recovery remain distinct transitions.
- **REQ-SEC-THREAT-014 — SHALL:** Supply-chain controls reject identity collision, substitution, downgrade, signature stripping, manifest replacement, trust-root substitution, and incomplete evidence.
- **REQ-SEC-THREAT-015 — SHALL:** Offline and removable-media imports use quarantine, bounded parsing, complete inventory checks, trust verification, revocation context, compatibility checks, and no automatic execution or activation.
- **REQ-SEC-THREAT-016 — SHALL:** Public-to-private and private-to-public information flows use explicit domain gateways and preserve source, destination, classification, transformation, approval, and receipt identity.
- **REQ-SEC-THREAT-017 — SHALL:** Publication Gateway remain separate from kOA Mediatheque admission, and its UCKK Publication Bridge shall not become a generic bypass around component ownership, disclosure policy, or external-destination authorization.
- **REQ-SEC-THREAT-018 — SHALL:** Native core correctness, authorization, policy, activation, deterministic rendering, kOA Mediatheque ingestion, recovery, and offline operation remain independent of generative AI and of UCKK availability.
- **REQ-SEC-THREAT-019 — SHALL:** External AI use remains explicit, removable, data-class constrained, provenance-bearing, non-authoritative, and unable to mutate authority or privileged state directly.
- **REQ-SEC-THREAT-020 — SHALL:** No-AI, consent, cultural-rights, audience, attribution, export, withdrawal, and steward-authority restrictions are enforced at ingest, storage, query, render, publication, synchronization, backup, export, federation, and AI boundaries.
- **REQ-SEC-THREAT-021 — SHALL:** SenTient remains optional, isolated, task activated, resource bounded, and non-authoritative.
- **REQ-SEC-THREAT-022 — SHALL:** Audit and observability collect the minimum classified evidence needed for accountability, diagnosis, verification, recourse, and recovery.
- **REQ-SEC-THREAT-023 — SHALL:** Access to protected audit evidence is itself authenticated, authorized, minimized, and audited.
- **REQ-SEC-THREAT-024 — SHALL NOT:** Public accountability receipts expose protected identities, secrets, restricted evidence, or unrelated private payloads.
- **REQ-SEC-THREAT-025 — SHALL:** Inputs, archives, decompression, recursion, queries, pagination, retries, queues, concurrency, storage growth, and processing time have explicit bounds.
- **REQ-SEC-THREAT-026 — SHALL:** Resource pressure preserves authority evaluation, cancellation, integrity, evidence, withdrawal, rollback, and recovery before optional heavy work.
- **REQ-SEC-THREAT-027 — SHALL:** Dependency and integration failure degrades only the affected capability and does not silently expand authority or remove core local operation.
- **REQ-SEC-THREAT-028 — SHALL:** Active verified local artifacts and minimum local capabilities remain usable offline within their declared trust, revocation-freshness, and profile envelope.
- **REQ-SEC-THREAT-029 — SHALL:** Stale trust, clock uncertainty, revocation uncertainty, and offline downgrade risk remain visible and policy governed.
- **REQ-SEC-THREAT-030 — SHALL:** Recovery, trust replacement, destructive restore, break-glass use, and protected key operations use stronger authentication, bounded authority, expiry, evidence, and separation of duties when required.
- **REQ-SEC-THREAT-031 — SHALL:** Backup, export, restore, migration, federation, mirror transfer, and sovereignty exit preserve identity, provenance, rights, revocation, supersession, authority, and evidence relationships.
- **REQ-SEC-THREAT-032 — SHALL:** A clean restore and credible exit remain possible without dependence on one original operator or one removable external integration.
- **REQ-SEC-THREAT-033 — SHALL:** Restoration and recovery revalidate trust, revocation, compatibility, authority, audience, rights, and active-state eligibility before activation.
- **REQ-SEC-THREAT-034 — SHALL:** Support bundles, logs, crash reports, receipts, and exported evidence exclude secrets and sanitize sensitive or cross-tenant content.
- **REQ-SEC-THREAT-035 — SHALL:** Security incidents preserve evidence and authority boundaries while containing affected capabilities and retaining unrelated valid service.
- **REQ-SEC-THREAT-036 — SHALL:** New components, integrations, profiles, artifact classes, gateways, privileged operations, external surfaces, and trust relationships undergo threat-model review before active adoption.
- **REQ-SEC-THREAT-037 — SHALL:** Threat review records affected assets, adversaries, entry points, trust boundaries, abuse cases, controls, failure behavior, residual risk, owners, tests, and evidence.
- **REQ-SEC-THREAT-038 — SHALL:** Profiles own concrete host hardening, process isolation, network exposure, hardware trust, orchestration, storage protection, resource limits, and recovery realization.
- **REQ-SEC-THREAT-039 — SHALL:** High-assurance claims use hardware-backed or independently equivalent trust, measured or verified boot, protected key custody, separation of duties, and attestation as declared by the profile.
- **REQ-SEC-THREAT-040 — SHALL:** Residual risks involving governance legitimacy, institutional capture, coercion, semantic disagreement, and social abuse remain explicit rather than being misrepresented as technically eliminated.
- **REQ-SEC-THREAT-041 — SHALL:** Critical security transitions produce classified machine-readable evidence with stable actor, subject, authority, operation, result, and correlation identities.
- **REQ-SEC-THREAT-042 — SHALL:** Every active security control claim maps to an applicable threat, decision, requirement, lock, owner, profile, test, evidence, and exception state.
- **REQ-SEC-THREAT-043 — SHALL:** A failed required security test blocks or degrades the affected claim without fabricating a broader system-wide failure or success state.
- **REQ-SEC-THREAT-044 — SHALL:** Ordinary Markdown security documentation uses registry, reference, structure, language, decision, requirement, lock, and traceability validation without an automatic file-content-hash requirement.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Threat review trigger

A threat review begins when a change introduces or materially alters:

- a component;
- a profile;
- a trust root;
- a signing key class;
- a privileged operation;
- an artifact class;
- a release channel;
- a gateway;
- a data classification;
- an audience;
- an external integration;
- an AI capability;
- a federation relationship;
- an offline bundle;
- a backup, export, restore, or recovery path;
- a public endpoint;
- a direct or indirect authority decision.

Documentation-only changes that do not alter behavior can use normal documentation validation.

### 6.2 Threat discovery

1. Identify the change owner and affected canonical contracts.
2. identify protected assets and data classifications.
3. identify human, service, workload, node, publisher, signer, tenant, environment, artifact, and authority identities.
4. draw the data, command, event, artifact, privilege, trust, and recovery flows.
5. mark every trust boundary.
6. select applicable adversary classes.
7. identify misuse, abuse, compromise, error, coercion, and failure scenarios.
8. map scenarios to existing threat IDs.
9. create a new threat ID only when the scenario is not represented.
10. record residual risk and recourse.

### 6.3 Control selection

1. Identify the canonical owner for each required control.
2. prefer prevention for authority fabrication, key compromise, cross-tenant access, and irreversible disclosure.
3. add detection and evidence for compromise that cannot be fully prevented.
4. define bounded failure and degradation.
5. preserve unrelated valid capabilities.
6. define rollback, forward repair, recovery, and exit.
7. define profile-specific realization separately.
8. define tests and evidence.
9. reject controls that depend only on prompts, conventions, hidden operator knowledge, or unverifiable external state.

### 6.4 Security decision closure

1. Resolve every implementation-affecting security choice through its canonical owner.
2. record accepted decisions and locks.
3. resolve component, profile, artifact, and release compatibility.
4. resolve required exceptions and expiry.
5. update threat-to-control traceability.
6. block active adoption while authority, ownership, or failure behavior remains ambiguous.
7. preserve dissent, limitations, and residual risk where applicable.

### 6.5 Implementation review

1. Verify identity and tenant binding.
2. verify interface authentication and authorization.
3. verify direct database access is absent.
4. verify input, archive, query, queue, retry, and storage bounds.
5. verify secrets and key boundaries.
6. verify network and privilege restrictions.
7. verify artifact and supply-chain handling.
8. verify audit classification and minimization.
9. verify offline, failure, and recovery behavior.
10. verify removal and exit behavior for optional dependencies.

### 6.6 Security test and evidence

1. Run applicable unit, component, cross-component, profile, lifecycle, security, operations, and exit tests.
2. record the exact environment, profile, artifact, release, authority, and exception state.
3. store classified evidence.
4. reject stale or unrelated evidence.
5. confirm every active claim has a complete traceability path.
6. keep failed, blocked, and degraded outcomes explicit.
7. repeat tests after a material threat, control, profile, artifact, or authority change.

### 6.7 Incident transition

`text
suspected
-> triaged
-> contained
-> authority and trust evaluated
-> evidence secured
-> affected capabilities isolated
-> remediation selected
-> rollback or forward repair
-> verification
-> recovery
-> review and control update
-> closed
`

Containment does not fabricate emergency authority.

Closure requires evidence, remediation state, residual risk, and follow-up ownership.

### 6.8 Emergency authority

1. Identify the exact emergency and affected capability.
2. authenticate the requester and approvers.
3. bind authority to the operation, target, scope, reason, and expiry.
4. preserve separation of duties where required.
5. execute through normal bounded interfaces when possible.
6. record before and after state.
7. revoke or expire emergency authority automatically.
8. review every use.
9. correct policy or design rather than normalizing permanent emergency access.

### 6.9 Recovery and clean restore

1. Start from a clean or independently verified environment.
2. verify backup or Sovereignty Bundle identity and inventory.
3. verify encryption, signatures, trust, revocation, rights, audience, and provenance.
4. restore identity and governance before dependent authoritative state.
5. restore component-owned state through owner contracts.
6. rebuild derived indexes and caches.
7. verify workflows, artifacts, rights, revocations, and evidence.
8. activate artifacts only through normal lifecycle authority.
9. prove that the original operator is not technically required when the exit claim applies.
10. record restore and workflow-resume evidence.

## 7. Failure and Degradation

### 7.1 Authority uncertainty

The affected operation enters blocked behavior.

Read-only inspection, cancellation, evidence, and recovery can remain available when independently authorized.

The system does not infer a permissive answer.

### 7.2 Identity or tenant uncertainty

Authoritative mutation stops.

The response avoids revealing whether a cross-tenant object exists.

Existing unrelated tenant operations continue when isolation remains verified.

### 7.3 Component compromise

The affected component is isolated by identity, network, store, and capability boundaries.

Direct writes to other components remain unavailable.

Recovery uses verified artifacts and component-owned restore procedures.

### 7.4 Trust or key compromise

The affected signing, authority, identity, or encryption scope freezes or restricts.

Revocation, replacement trust, artifact impact, active-state treatment, offline distribution, and incident evidence follow their separate lifecycle contracts.

### 7.5 Artifact verification failure

The candidate remains quarantined, rejected, or inactive.

The previous compatible non-revoked artifact remains available when safe.

### 7.6 Audit degradation

Required local evidence is retained before a critical transition reports completion.

Remote forwarding can queue within bounds.

Optional diagnostic detail can reduce before critical evidence.

### 7.7 Resource exhaustion

New heavy work, advisory processing, indexing, synchronization, or optional integrations stop first.

Authority, cancellation, withdrawal, rollback, evidence, minimum local operation, and recovery remain prioritized.

### 7.8 Network partition

Active verified local state remains usable within the offline envelope.

Remote identity, federation, integration, mirror, publication, and revocation refresh become explicitly unavailable or stale.

The interface exposes freshness and unavailable capabilities.

### 7.9 External AI or integration failure

Only the assistive or connected capability degrades.

Core local identity, policy, workflow, deterministic rendering, media ingestion, active Kristal query, artifact verification, and recovery remain available according to profile.

### 7.10 Recovery failure

Partial restore does not become a successful recovery claim.

The clean target remains isolated.

The last valid source or backup remains preserved, and the process enters rollback, forward repair, or manual recovery with evidence.

### 7.11 Governance capture

Technical controls preserve rule identity, history, approvals, dissent, receipts, forkability, and exit.

They do not declare the captured policy legitimate.

Affected communities and operators retain recourse paths defined outside this threat model.

### 7.12 Irreversible disclosure

The system stops further distribution, propagates withdrawal where possible, revokes or supersedes affected artifacts, purges authorized caches, records impact, and preserves minimal lawful evidence.

It does not claim that previously copied public data can always be recovered.

## 8. Cross-Component Interactions

| Interaction | Threat focus | Required boundary |
| --- | --- | --- |
| Konnaxion → Orgo | Untrusted public input, Sybil abuse, cross-domain mutation | Explicit intake, classification, provenance, authorization, rate limits, no shared store |
| Orgo → Publication Gateway → Konnaxion | Private-data leakage, redaction failure, duplicate publication | Exact candidate, policy, transformation, approval, idempotent delivery, receiving receipt, withdrawal |
| Local files → kOA Mediatheque admission | Parser abuse, path traversal, malicious media, rights loss | User selection, quarantine, bounded parsing, original preservation, and rights review |
| kOA Mediatheque → Publication Gateway + UCKK adapter → external UCKK Moodle | Unauthorized disclosure, destination confusion, credential theft, replay, remote rejection | Explicit publication request, disclosure authorization, authenticated destination, manifest, idempotency, and receipt |
| GF Wordbench → SemantiK | Toolchain contamination, runtime mutation, incompatible language artifact | Fixed build, validation, immutable pack, independent runtime verification and activation |
| SenTient → owning review workflow | Candidate laundering, hidden authority, resource exhaustion | Isolated task, candidate status, provenance, uncertainty, human review, no direct writes |
| External AI → local owner | Sensitive-data exfiltration, hallucinated authority, provider lock-in | Explicit initiation, data eligibility, no-AI policy, provenance, candidate status, removability |
| Artifact repository → runtime owner | Substitution, downgrade, stale trust, partial publication | Immutable identity, signatures, revocation, compatibility, quarantine, staging, activation authority |
| Governance Policy Runtime → governed component | Policy replay, stale decision, scope confusion | Operation binding, identity, expiry, obligations, evidence, fail-closed behavior |
| kOA Node Agent → host | Root abuse, arbitrary command execution, replay | Allowlisted schema, operation-bound decision, narrow target, timeout, before/after verification, receipt |
| Audit Broker ← all components | Privacy collapse, missing evidence, authorization capture | Classified evidence, minimization, protected access, no authorization role, independent retention |
| Resource Governor → components | Governance capture through resource decisions | Deterministic resource policy, separate authority, bounded degradation, observable reason |
| Backup/export → clean restore | Data loss, trust replacement, exit lock-in | Complete inventory, encryption, trust handover, independent verification, owner restore, no implicit activation |
| Federation peer ↔ local domain | Replay, conflicting authority, deceptive identity | Peer identity, authority scope, sequence, provenance, local admission, conflict preservation |
| Profile/control plane → node | Hidden orchestration, excessive exposure, drift | Explicit profile membership, topology, hardware, network, resource, orchestration, attestation, evidence |

Every interaction inherits the owner component's detailed contract.

## 9. Decision Closure and Prohibited Assumptions

### 9.1 Closed decisions

| Decision | Closed security rule |
| --- | --- |
| `DEC-AUTH-001` | Authority is explicit, scoped, operation-bound, expiring where applicable, and never inferred from authentication or access alone. |
| `DEC-IDENT-001` | Human, role, organization, tenant, node, workload, publisher, signer, artifact, environment, and authority identities remain distinct. |
| `DEC-DATA-001` | Authoritative data domains have one owner and cross-component direct writes are prohibited. |
| `DEC-COMP-001` | Components interact through explicit contracts with declared failure and evidence behavior. |
| `DEC-GOV-001` | Governance Policy Runtime decides governed policy; Resource Governor and other components retain separate responsibilities. |
| `DEC-PRIV-001` | Accountability uses selective disclosure, classified evidence, minimization, rights, and recourse rather than unrestricted transparency. |
| `DEC-AI-001` | AI remains optional, explicit, removable, non-authoritative, and unable to grant privilege or authority directly. |
| `DEC-LIFE-001` | Artifact verification, release, activation, rollback, revocation, and evidence remain separate across independent channels. |
| `DEC-GATE-001` | Local media admission and cross-domain publication are separate security boundaries; the UCKK adapter is subordinate to Publication Gateway authorization. |
| `DEC-SENT-001` | SenTient remains isolated, task activated, and non-authoritative. |
| `DEC-MEDIATHEQUE-001` | kOA Mediatheque ingestion and identity remain deterministic and preserve original media. |
| `DEC-UCKK-EXT-001` | UCKK remains an external online Moodle and Mediatheque authority with separate storage and controlled directional interchange. |
| `DEC-ARI-001` | Ariane guidance and automation remain deterministic, user-controlled, and independent of optional voice. |
| `DEC-LANG-001` | GF Wordbench build authority remains separate from SemantiK runtime activation. |
| `DEC-KRISTAL-001` | Kristal is an epistemic foundation, not a workflow authority or universal operational database. |
| `DEC-HW-001` | High-assurance profiles can require hardware-backed trust and attestation without imposing it on every profile. |

### 9.2 Prohibited assumptions

Authors, implementers, validators, operators, and AI agents do not assume that:

- authentication grants authorization;
- repository access grants signing or release authority;
- signing grants compatibility or activation authority;
- publication means active;
- a valid signature means safe;
- a newer artifact is authorized or compatible;
- a public record is safe for private admission;
- a private record is safe for public disclosure;
- one database can serve multiple component authorities without explicit ownership;
- a service account is tenant neutral;
- a shared host implies shared trust;
- root access is an ordinary API;
- an emergency account can remain permanent;
- an audit system can expose every detail;
- missing classification means public;
- missing consent means permission;
- cultural authority can be inferred from absence of objection;
- AI confidence is evidence;
- a local model is trusted because it is local;
- a connected integration is harmless because it is optional;
- a cache or index is authoritative;
- online reachability establishes trust;
- removable-media possession establishes trust;
- offline operation establishes current revocation knowledge;
- restore can reactivate prior authority automatically;
- backup possession grants key or activation authority;
- a clean export is complete without restore testing;
- Kubernetes is a universal endpoint security requirement;
- one profile's hardening choice applies globally;
- technical controls prove governance legitimacy or factual truth;
- ordinary Markdown security files require content hashes.

A new security-sensitive implementation choice remains inactive until its canonical owner closes authority, ownership, failure behavior, tests, and evidence.

## 10. Validation Criteria

| Validation group | Required tests |
| --- | --- |
| Authority, privilege, and identity | `TEST-SEC-001`, `TEST-SEC-002`, `TEST-SEC-003`, `TEST-SEC-004`, `TEST-SEC-005`, `TEST-SEC-006`, `TEST-SEC-007`, `TEST-CROSS-007`, `TEST-CROSS-008`, `TEST-CROSS-009`, `TEST-CROSS-014`, `TEST-SYS-004` |
| Keys, supply chain, and lifecycle | `TEST-SEC-008`, `TEST-SEC-015`, `TEST-LIFE-001`, `TEST-LIFE-002`, `TEST-LIFE-003`, `TEST-LIFE-004`, `TEST-LIFE-005`, `TEST-LIFE-006`, `TEST-LIFE-007`, `TEST-LIFE-008`, `TEST-LIFE-009`, `TEST-LIFE-010`, `TEST-LIFE-011`, `TEST-LIFE-012`, `TEST-LIFE-013`, `TEST-LIFE-014`, `TEST-LIFE-015` |
| Tenant, domain, and gateway separation | `TEST-SEC-009`, `TEST-SEC-010`, `TEST-CROSS-001`, `TEST-CROSS-002`, `TEST-CROSS-003`, `TEST-CROSS-004`, `TEST-CROSS-005`, `TEST-CROSS-006`, `TEST-CROSS-010`, `TEST-CROSS-015`, `TEST-SYS-013`, `TEST-SYS-014` |
| Privacy, audit, rights, and AI | `TEST-SEC-011`, `TEST-SEC-012`, `TEST-SEC-013`, `TEST-SEC-014`, `TEST-CROSS-011`, `TEST-CROSS-012`, `TEST-CROSS-013`, `TEST-SYS-002`, `TEST-SYS-003`, `TEST-SYS-006`, `TEST-SYS-007`, `TEST-SYS-008`, `TEST-SYS-009`, `TEST-SYS-012` |
| Offline, resources, and degradation | `TEST-SYS-001`, `TEST-SYS-005`, `TEST-SYS-010`, `TEST-SYS-015`, `TEST-PROF-005`, `TEST-PROF-006`, `TEST-PROF-007`, `TEST-PROF-008`, `TEST-PROF-010`, `TEST-OPS-001`, `TEST-OPS-002`, `TEST-OPS-003`, `TEST-OPS-006`, `TEST-OPS-010` |
| High-assurance and profile realization | `TEST-PROF-001`, `TEST-PROF-002`, `TEST-PROF-003`, `TEST-PROF-004`, `TEST-PROF-009`, `TEST-PROF-013`, `TEST-PROF-014`, `TEST-PROF-015` |
| Operations, incident response, and recovery | `TEST-SYS-011`, `TEST-OPS-004`, `TEST-OPS-005`, `TEST-OPS-007`, `TEST-OPS-008`, `TEST-OPS-009` |
| Exit and independent restoration | `TEST-EXIT-001`, `TEST-EXIT-002`, `TEST-EXIT-003`, `TEST-EXIT-004`, `TEST-EXIT-005`, `TEST-EXIT-006`, `TEST-EXIT-007`, `TEST-EXIT-008` |
| Documentation and traceability | `TEST-DOC-VAL-003`, `TEST-DOC-VAL-005`, `TEST-DOC-VAL-006`, `TEST-DOC-VAL-007`, `TEST-DOC-VAL-008`, `TEST-DOC-VAL-009`, `TEST-DOC-VAL-010`, `TEST-DOC-VAL-012`, `TEST-DOC-VAL-016`, `TEST-DOC-VAL-017`, `TEST-DOC-VAL-018`, `TEST-DOC-VAL-019`, `TEST-DOC-VAL-020` |

Threat-model validation additionally confirms:

1. all asset, adversary, boundary, and threat identifiers are unique;
2. every threat identifies affected assets, primary controls, and residual risk;
3. every global control has one canonical owner;
4. every active component resolves in `generated/component-catalog.json`;
5. authoritative data domains have one owner;
6. direct cross-component database mutation is absent;
7. identity, tenant, audience, environment, and authority scope are explicit;
8. privilege is schema bound and no arbitrary root interface exists;
9. protected keys remain outside ordinary workspaces and workers;
10. external AI and SenTient remain non-authoritative and removable;
11. public/private and local-media gateways remain distinct;
12. offline imports and restores use bounded parsing and no automatic activation;
13. resource pressure preserves critical security work;
14. evidence remains classified, minimized, durable, and protected;
15. backup, export, restore, withdrawal, revocation, and exit are tested;
16. high-assurance claims match the high-assurance profile;
17. every requirement maps to an active test or approved manual control;
18. every active claim has current traceability and evidence;
19. exceptions are explicit, scoped, compensating, approved, and expiring;
20. no unresolved authority marker exists;
21. all active prose is in English.

A failed required test blocks or narrows the affected claim.

It does not create a fabricated claim that unrelated components are unsafe or unavailable.

## 11. Non-Normative Examples

### 11.1 Compromised public service

An attacker compromises a Konnaxion service process.

The process cannot write Orgo, Kristal, governance, identity, or audit stores directly. Network and database credentials limit lateral movement. Public-service evidence identifies the affected workload and requests.

The incident isolates Konnaxion while private Orgo work and active local Kristal consultation continue.

### 11.2 Malicious language artifact

A repository serves a modified compiled language pack under a familiar filename.

SemantiK verifies immutable identity, manifest, inventory, signer scope, revocation, release channel, and compatibility. Verification fails, the pack remains quarantined, and the prior known-good language pack remains active.

The filename does not grant trust.

### 11.3 Policy capture attempt

An administrator proposes a policy bundle that silently expands emergency authority and reduces publication review.

The governance release displays the semantic difference, required approvals, expiry, affected threats, tests, and evidence. The policy remains independently versioned and contestable.

A formally approved harmful policy remains a governance residual risk rather than a technical success claim.

### 11.4 Public/private disclosure error

Orgo produces a report containing a protected witness identity.

Publication Gateway classification and minimization detect the restricted field. The candidate remains blocked until an authorized transformation removes it and the required reviewer approves the exact public output.

The private Orgo result remains unchanged.

### 11.5 External AI assistant

A user explicitly sends eligible public text to an approved external AI service for a candidate summary.

The request records provider, purpose, and provenance. The returned text has no publication or authority status. A local reviewer either admits a corrected version or rejects it.

No private Orgo evidence or no-AI material is mounted into the external service path.

### 11.6 Offline downgrade

A sovereign node receives an older but validly signed governance bundle from removable media.

The importer compares release sequence, revocation epoch, authority release, and downgrade policy. The candidate is rejected or requires an explicit emergency path with visible risk and expiry.

The active governance bundle remains unchanged.

### 11.7 Resource exhaustion

An attacker submits many expensive queries and malformed archives.

Rate limits, parser bounds, queue limits, cancellation, and Resource Governor reduce optional work. Authority evaluation, withdrawal, evidence, active deterministic queries, and recovery remain prioritized.

The interface exposes degraded capability rather than silently dropping critical actions.

### 11.8 Recovery capture attempt

An operator tries to restore a Sovereignty Bundle while substituting a new trust root and reusing old activation state.

Independent verification detects the trust mismatch. The clean target remains isolated. New environment enrollment and normal artifact activation are required.

Possession of the backup does not grant activation authority.

### 11.9 Cultural withdrawal

A community steward withdraws authority for a restricted media and Kristal artifact set.

Governed withdrawal updates audience packs, public derivatives, indexes, caches, federation records, exports, and AI access. Audit retains only the minimal lawful evidence.

The system does not claim that unauthorized external copies can always be erased.

### 11.10 Credible exit

A tenant receives a signed Sovereignty Bundle with identity, governance, component exports, Kristal artifacts, rights, evidence, trust handover, and restore tests.

An independent operator restores it on a clean compatible node, rebuilds derived state, resumes Orgo workflows, preserves withdrawn content status, and verifies provenance.

The original operator is not technically required for the successful restore.
