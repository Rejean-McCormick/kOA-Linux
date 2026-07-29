# Offline Bundles

## 1. Purpose

Offline Bundles carry releases, policies, trust updates, Kristal artifacts, synchronization payloads, or recovery material across disconnected boundaries.

## 2. Bundle classes

- OS update bundle;
- service update bundle;
- Governance Policy Bundle package;
- Kristal distribution bundle;
- revocation/trust update bundle;
- synchronization bundle;
- Sovereignty Bundle;
- recovery bundle.

## 3. Required envelope

Every bundle declares:

- bundle class and version;
- issuer and intended audience;
- tenant, environment, and channel scope;
- creation and expiry information with clock assumptions;
- payload inventory and hashes;
- dependencies and compatibility;
- confidentiality/encryption metadata;
- replay and sequence protection;
- signatures.

## 4. Import sequence

```text
media detection
  → copy to quarantine
  → parse bounded manifest
  → verify signature and trust scope
  → verify inventory and size limits
  → scan/validate payload by class
  → check replay, expiry, revocation, compatibility
  → policy decision
  → stage
  → explicit activation or synchronization
```

## 5. Media threats

The importer MUST defend against path traversal, symlink escape, decompression bombs, oversized manifests, parser ambiguity, duplicate names, device spoofing, stale signed content, and malicious optional metadata.

## 6. Confidential bundles

Sensitive bundles SHOULD be encrypted to tenant or node recipients. Signature verification and decryption errors fail closed. Decrypted material is not left in shared temporary paths.

## 7. Receipts

Import and activation are separate receipted events. A valid bundle may be installed but not authorized for activation.
