# Koali Technical Maturity Assessment

**Assessment date:** 2026-08-27  
**Current status:** Advanced Beta — Integration Hardening  
**Estimated engineering maturity:** ~80%  
**Estimated Release Candidate readiness:** ~60–65%

> This assessment is a technical maturity checkpoint. It is not a Release Candidate declaration and the percentages are engineering estimates, not mathematical completion metrics.

## Executive summary

Koali has moved well beyond the prototype stage. Its architecture, contracts, component model, release engineering, host integration, validation framework, and operational model are substantially implemented.

The remaining work is concentrated in system closure and qualification: runtime wiring, reproducible system-image production, machine-level validation, security confinement, offline operation, recovery, rollback, and complete release evidence.

The most accurate current classification is:

**Advanced Beta — Integration Hardening**

## Scope

Koali is the current name for the project lineage previously referred to as:

- kOA-Linux
- kOA Digital Ecosystem
- Sociotechnical OS

This assessment is primarily based on the inspected kOA-Linux implementation snapshot and its validation evidence.

## Maturity by area

| Area | Estimated maturity |
|---|---:|
| Architecture and contracts | 95% |
| Internal components | 85–90% |
| Interfaces and adapters | 80–85% |
| Component-level testing | 90% |
| Packaging and release engineering | 75–80% |
| Linux host, boot and recovery | 70–75% |
| Runtime wiring | 55–65% |
| End-to-end system integration | 50–60% |
| Security and offline qualification | 40–50% |
| Overall engineering maturity | ~80% |
| RC readiness | ~60–65% |

## Strongest areas

### Architecture and contracts

Koali has a mature contract-first architecture with:

- explicit component boundaries;
- ownership rules;
- capability and health/readiness contracts;
- profile-driven behavior;
- fail-closed semantics;
- governance and security boundaries;
- release-channel separation;
- explicit authority separation.

### Components

The implementation includes substantial work across components such as:

- Audit Broker;
- Governance Policy Runtime;
- Identity and Trust;
- kOA Mediatheque;
- kOA Node Agent;
- Kristal Runtime;
- Publication Gateway;
- Resource Governor.

The inspected code includes real domain layers, application services, adapters, persistence logic, migrations, APIs, and packaging.

### Host and release engineering

The repository includes machinery for:

- root filesystem construction;
- boot artifacts;
- disk-image construction;
- recovery artifacts;
- image sealing and verification;
- release manifests and Release Sets;
- promotion and rollback;
- SBOM and provenance;
- release candidate construction;
- offline and security gates.

This is significantly more mature than a conventional early beta codebase.

## Test and validation state

The inspected codebase contains a substantial test surface.

During the assessment:

- 986 tests across components, integrations, interfaces, assembly, operations, and tools passed;
- the central non-QEMU conformance suite produced 239 passes, 22 failures, and 2 skips.

The remaining failures were concentrated around system integration concerns such as:

- generated locks or inventories out of sync;
- session packaging;
- integration alignment;
- reproducibility;
- system-image pipeline consistency;
- generated projections.

This indicates a late integration phase rather than an early implementation phase.

## Main blockers before pre-RC

Koali should not yet be classified as pre-RC because the complete appliance has not yet been fully qualified.

The main remaining requirements are:

1. eliminate remaining non-QEMU conformance failures;
2. complete runtime wiring for the Node Agent and privileged broker;
3. build a reproducible system image;
4. boot that image successfully;
5. pass QEMU system validation;
6. pass machine-observed security and confinement validation;
7. pass offline validation;
8. prove recovery and last-known-good behavior;
9. produce a complete Release Set;
10. sign, verify, activate, and roll back that Release Set with complete evidence.

## Release interpretation

Koali is largely built as an engineering system.

The main challenge is now to prove the whole system as a reproducible, governed, bootable appliance.

> **Koali: the system is largely built, but the release still needs to be proven.**

## Recommended public status

**Advanced Beta — Integration Hardening**

Suggested short description:

> Koali has reached an advanced engineering beta. Core architecture, contracts, components, release engineering and system validation infrastructure are substantially implemented. Current work focuses on runtime integration, system-image qualification, security, offline operation, recovery and end-to-end release evidence. This is not yet a Release Candidate.
