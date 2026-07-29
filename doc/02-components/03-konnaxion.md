# Principal Domain — Konnaxion

## 1. Role

Konnaxion is the principal public and commons-oriented plane of kOA. It provides discovery, education, collaboration, deliberation, cultural exchange, public knowledge surfaces, collective curation, and distribution.

## 2. Architecture

The existing product stack is a modular web platform. The target kOA Linux architecture preserves Konnaxion's own global application layout and route/module structure while hosting it inside the wider `koa-session-shell`.

Konnaxion SHOULD remain a modular monolith or coherent application group with explicit module APIs. It MUST NOT be split into network services merely to satisfy an architectural fashion.

## 3. Kristal responsibilities

Konnaxion owns the user-facing functions for:

- browsing and searching Runtime Packs;
- selecting and explaining reader policies;
- showing validation, certainty, authority, and disagreement labels;
- offline delivery and cache status;
- requesting pack installation/activation;
- displaying stale, provisional, contested, expired, or revoked states;
- collecting non-mutating feedback signals;
- distributing approved public artifacts.

Konnaxion does not own Kristal content identity or validation semantics.

## 4. Relationship with Orgo

Konnaxion sends structured signals, submissions, public decisions, requests, and feedback to Orgo through contracts. It receives approved non-sensitive publications and execution summaries through the Publication Gateway.

Konnaxion MUST NOT access Orgo's private persistence directly.

## 5. SmartVote and EkoH

Where SmartVote is used, Konnaxion MUST preserve explicit readings rather than compressing all authority into one hidden score. At minimum, the baseline and advisory weighted results remain distinguishable. Weighting rules are versioned, domain-bounded, explainable, and contestable.

SmartVote MUST NOT map directly to Linux roles, root privilege, signing authority, or node activation.

## 6. Offline behavior

When offline, Konnaxion MUST:

- serve active verified local content;
- display synchronization age and trust status;
- queue idempotent permitted actions;
- avoid activating artifacts that require unavailable trust material;
- continue local navigation and search within the declared capability envelope;
- preserve user work for later synchronization.

## 7. Security

Konnaxion runs in the public security domain. It uses separate credentials, storage, network, and caches from Orgo. Public input is untrusted and MUST pass validation, rate limiting, content controls, and workflow gates before it can influence trusted artifacts or operations.

## 8. Observability

Konnaxion emits operational metrics and receipts, not raw private knowledge by default. Feedback about pack use or errors creates Orgo work or distribution adjustments; it MUST NOT mutate Kristal Exchange directly.
