# Rollback and Recovery

## 1. Rollback classes

- OS deployment rollback;
- service bundle rollback;
- Governance Policy Bundle rollback;
- Runtime Pack rollback;
- configuration rollback;
- data restore;
- trust-root recovery.

Each class has different safety semantics. A common button MUST NOT hide those differences.

## 2. Triggers

Rollback MAY be triggered by:

- explicit authorized operator action;
- failed health acceptance;
- verified revocation;
- repeated runtime errors crossing a declared threshold;
- failed migration checkpoint;
- incident-response workflow.

The same verified trigger sequence and state SHOULD produce the same rollback decision.

## 3. Authorization

Rollback is governed. Downgrading below security or revocation floors requires a separate emergency policy, stronger approval, and visible risk receipt.

## 4. Known-good retention

Nodes retain at least:

- active state;
- previous known-good state;
- recovery environment;
- required manifests and signatures;
- migration and rollback metadata.

## 5. Data recovery

Restore uses a clean compatibility check, not blind file replacement. The system verifies tenant, schema, artifact, encryption, and trust dependencies before committing restored state.

## 6. Trust recovery

Trust-root replacement is one of the highest-impact operations. It SHOULD require dual control, physical or out-of-band evidence, a continuity statement, and post-event audit.

## 7. Recovery test

Every supported node profile MUST have an automated or rehearsed test proving that a failed update, corrupted active pack, unavailable network, and lost application service can reach a safe recoverable state.
