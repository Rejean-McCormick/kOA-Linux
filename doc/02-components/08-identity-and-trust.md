# Identity and Trust

## 1. Identity layers

kOA distinguishes:

- human identity;
- pseudonymous participation identity;
- organization and tenant identity;
- role and delegation identity;
- node identity;
- service workload identity;
- publisher and signer identity;
- authority-channel identity;
- artifact content identity.

These identities MUST NOT be collapsed into one universal identifier.

## 2. Authentication

Local authentication MUST remain possible for declared offline use. Deployments MAY federate identity online, but MUST define cached credential, expiry, revocation, and emergency behavior.

High-impact operations SHOULD require phishing-resistant factors or hardware-backed credentials.

## 3. Authorization

Authorization combines authenticated attributes, tenant, action, resource, policy version, workflow state, and node context. Unix group membership alone is insufficient for governance authorization.

## 4. Node identity

A node has a stable public identity and rotatable keys. TPM-backed keys SHOULD be used for enhanced assurance. Node replacement and key loss require a governed re-enrollment workflow.

## 5. Trust roots

Trust roots are scoped by:

- tenant;
- environment;
- release channel;
- artifact type;
- authority domain.

A signature valid under another tenant or environment MUST NOT be accepted automatically.

## 6. Key separation

Separate keys SHOULD exist for:

- OS release signing;
- service release signing;
- policy bundle signing;
- Kristal publishing;
- authority recognition;
- node identity;
- audit anchoring;
- export encryption.

## 7. Revocation

Revocation information MUST be distributable offline in signed, versioned form. Nodes record the newest accepted revocation epoch and apply downgrade protection.

## 8. Delegation and recourse

Role delegation is explicit, scoped, time-bounded, and revocable. Decisions retain the identity of both delegator and acting subject where appropriate. Identity challenges and corrections use a defined recourse workflow rather than silent operator edits.
