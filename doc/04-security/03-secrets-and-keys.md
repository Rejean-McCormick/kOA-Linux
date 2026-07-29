# Secrets and Keys

## 1. Key classes

- OS release signing;
- service bundle signing;
- Governance Policy Bundle signing;
- Kristal publisher signing;
- authority recognition signing;
- node identity;
- workload identity;
- audit anchoring;
- tenant data encryption;
- offline/export encryption;
- recovery.

Keys of different classes MUST NOT be reused merely for convenience.

## 2. Custody

Private release and authority keys SHOULD be held outside application nodes, preferably in an HSM, hardware token, or threshold-signing system. Build workers produce hashes and attestations, not unrestricted signing authority.

## 3. Node secrets

Node secrets SHOULD be hardware-bound where available. Services receive only the secrets required for their purpose, through protected files, credentials APIs, or secret stores—not environment variables exposed broadly.

## 4. Rotation

Every key class has issuance, activation, overlap, rotation, revocation, compromise, archival, and destruction procedures. Verification supports declared overlap without accepting indefinite old keys.

## 5. Backup and recovery

Key backup is encrypted, access-controlled, tested, and separated from ordinary data backup. Recovery of a key does not automatically authorize its continued use; policy may require reissuance.

## 6. Compromise

A suspected signing-key compromise triggers channel freeze, revocation publication, artifact review, replacement trust material, and incident receipts. Offline distribution of revocation is part of the response plan.

## 7. Secrets in logs and exports

Secrets, raw tokens, private keys, and unredacted credentials MUST NOT enter logs, audit receipts, crash reports, or Sovereignty Bundles unless the bundle explicitly uses a protected key-handover profile.
