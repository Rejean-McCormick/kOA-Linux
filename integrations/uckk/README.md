# UCKK directional integration boundary

This directory contains the kOA-owned boundary for controlled interchange with
the external UCKK Moodle platform. UCKK is not a kOA-Linux subsystem and is not
required for local or offline kOA Mediatheque operation.

Two independent directions are declared and must remain separate:

- `publish_to_uckk`: an explicitly selected and Publication Gateway-authorized
  local record version is packaged and transported to an allowlisted UCKK
  destination; remote success exists only after a validated publication receipt.
- `import_from_uckk`: an explicitly selected UCKK learning package is retrieved
  or received, quarantined, verified, and submitted for explicit local
  acceptance; acceptance creates separate kOA record and version identities.

The directions have separate contracts, credentials, operation allowlists,
queues, packages, receipts, retries, reconciliation, and degradation states.
There is no generic synchronization interface, no direct database access, no
remote overwrite of accepted local records, and no transfer of source authority.
The shared Mediatheque frame provides compatible representation only.

## Activation state

The canonical directional contracts and their local compatibility pins are
present. The authoritative UCKK platform repository or release, immutable
revision, source digest, license metadata, and documentation release are not
provided by the active corpus. `source.lock.json` therefore records an explicit
blocked external-source state. Preparation and local contract testing are
permitted; activation is not.

## Public implementation boundary

The adapter package exposes only kOA-owned public boundary types. Existing
publication code implements `publish_to_uckk`; inbound import modules are owned
by the separate import bundle. Deployment transports, credentials, storage,
quarantine, and owner APIs are injected through declared interfaces.

## Validation

From the repository root:

```bash
PYTHONPATH=integrations/uckk/adapter/src python -m compileall -q \
  integrations/uckk/adapter/src/koa_uckk_adapter
PYTHONPATH=integrations/uckk/adapter/src python -m pytest -q \
  integrations/uckk/tests/test_contract.py integrations/uckk/tests/test_health.py
python docs/tools/check_uckk_external_boundary.py
python docs/tools/check_greenfield_architecture.py
```
