# Operating-System Updates

## 1. Image model

The OS is built as an immutable signed image. The reference implementation SHOULD use bootc/OSTree or an equivalent maintained image mechanism with atomic deployment and rollback.

## 2. Build pipeline

```text
source and lockfiles
  → reproducible image build
  → SBOM and provenance
  → security and integration tests
  → image signature
  → Release Set binding
  → registry/offline publication
```

## 3. Staging

A node stages an image without changing the active boot. It verifies:

- signature and trust scope;
- image digest;
- Release Set compatibility;
- hardware and node profile;
- required storage space;
- required migration prerequisites;
- revocation and downgrade state.

## 4. Activation

Activation is requested through policy and performed by `koa-node-agent`. The node records the expected new boot identity and previous known-good deployment.

## 5. Boot health

A new image is accepted only after required services, storage, policy runtime, active artifacts, and graphical/session checks pass. Failure causes automatic or operator-approved rollback according to profile.

## 6. Offline update

An offline OS bundle contains the image, signatures, Release Set, revocation information, compatibility metadata, and import instructions. The node MUST NOT trust removable media merely because it is physically present.

## 7. Emergency security update

Emergency update policy MAY shorten ordinary approval, but MUST preserve signature, compatibility, receipt, rollback, and post-event review. Emergency authority expires automatically.

## 8. Drift control

Production nodes MUST report or locally expose whether the running image matches a signed release identity. Undocumented local mutation is a conformance failure.
