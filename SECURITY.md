# Security Policy

## Supported releases

Security support applies only to a complete, signed, verified Release Set whose lifecycle status and support decision are active in the canonical release records.

This greenfield repository snapshot does not declare a published runtime Release Set. Source branches, pull requests, development artifacts, unsigned packages, incomplete channel combinations, and unverified offline bundles are not supported releases merely because they are available.

When release infrastructure is present, support status must be derived from the active release contracts and records, not from this file, a branch name, a mutable tag, or a directory name.

## Report a vulnerability privately

Do not open a public issue for a suspected vulnerability.

Use the repository host's private security-reporting feature when it is enabled. If no private reporting feature is available, contact the maintainers through an already established private project channel. The supplied authority does not declare a public security email address, so this file does not invent one.

Do not include production credentials, private keys, access tokens, personal data, decrypted recovery material, or unnecessary governed content. Provide minimized evidence sufficient to reproduce and assess the issue.

A useful report includes:

- affected component, integration, profile, artifact, or release identity;
- exact version, commit, digest, or Release Set reference;
- deployment profile and relevant operating mode;
- impact and prerequisites;
- reproducible steps or a minimal proof of concept;
- observed and expected behavior;
- relevant logs with secrets and governed payloads removed;
- any known containment or recovery action.

## Handling process

Maintainers should:

1. acknowledge the private report through the same private channel;
2. establish the affected authority owner and scope;
3. preserve evidence without broadening disclosure;
4. classify whether the issue affects source, build, artifact, release, activation, runtime, recovery, or trust state;
5. reproduce the issue in an isolated environment using non-production identities and data;
6. prepare a bounded correction, validation plan, and rollback or forward-repair path;
7. publish updated artifacts, evidence, revocation information, or operational guidance through the governed release process when required;
8. coordinate public disclosure only after affected users have an actionable protected path.

No response-time promise is declared by the supplied authority. Reporters must not interpret silence as permission to disclose secrets or exploit production systems.

## Scope priorities

Reports are especially relevant when they concern:

- identity, trust roots, signatures, key custody, or revocation;
- privilege boundaries, broker operations, path traversal, sandboxing, capabilities, seccomp, LSM, or polkit;
- cross-component data access or authority transfer;
- release, update, offline import, activation, rollback, restore, or recovery integrity;
- secret exposure, privacy, selective audit, or support-bundle redaction;
- external integration boundaries or unaccepted candidate content;
- resource-exhaustion behavior that can bypass declared limits;
- generated-content, dependency, source-pin, or provenance substitution.

## Safe research expectations

Do not access data or systems beyond the authorization provided to you. Do not cause persistent service disruption, alter authoritative data, weaken trust state, or retain secrets. Stop testing when continued activity could affect users or production authority.

This policy is operational guidance. Canonical security controls and release requirements remain in the contracts and owning normative documents under `docs/`.
