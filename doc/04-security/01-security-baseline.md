# Security Baseline

## 1. Host baseline

- maintained standard kernel and firmware;
- Secure Boot where supported;
- immutable signed OS image;
- full-disk or volume encryption for durable sensitive state;
- SELinux enforcing or equivalent mandatory access control;
- minimal installed packages;
- automatic security update workflow with rollback;
- restricted local console and recovery;
- accurate inventory of active release identities.

## 2. Service baseline

- dedicated service identities;
- rootless containers where feasible;
- no privileged containers;
- read-only root filesystem;
- dropped Linux capabilities;
- `NoNewPrivileges`;
- seccomp and LSM confinement;
- explicit writable mounts;
- resource quotas;
- default-deny network;
- structured logs and health checks;
- secrets by reference, never embedded in images.

## 3. Application baseline

- strong session management;
- tenant context on every request;
- authorization at service boundaries;
- CSRF, XSS, SSRF, injection, and upload protections;
- idempotency for retryable writes;
- rate limiting and abuse controls;
- bounded parsers and payload size;
- safe error messages that do not reveal cross-tenant existence;
- security headers and origin restrictions.

## 4. Privileged operation baseline

- allowlisted node-agent operations;
- policy decision binding;
- replay protection;
- before/after state verification;
- operation timeout and cancellation;
- decision and operation receipts;
- dual control for trust roots, release signing, and destructive recovery at high assurance.

## 5. Development baseline

- code review and protected branches;
- dependency lockfiles;
- secret scanning;
- SAST and dependency vulnerability scanning;
- container and IaC scanning;
- reproducible builds where feasible;
- signed commits/tags for release inputs;
- threat-model review for new trust boundaries;
- conformance tests in CI.

## 6. Vulnerability response

Every component has an owner, supported versions, update path, and severity process. A vulnerability that invalidates trust or artifact safety may trigger revocation, emergency policy, or channel freeze.
