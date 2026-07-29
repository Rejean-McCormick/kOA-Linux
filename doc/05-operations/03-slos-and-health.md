# SLOs and Health

## 1. SLO model

SLOs are defined by capability and node profile, not only by service uptime.

Representative endpoint objectives:

- local session start success;
- active Kristal query availability while offline;
- local Orgo critical-work availability;
- policy decision latency;
- signed activation success;
- rollback success;
- synchronization recovery after reconnect;
- backup and exit restore success.

## 2. Suggested initial targets

These are engineering starting points, not established production commitments:

- local policy decision p95 under 100 ms for ordinary rules;
- local Kristal query p95 under 250 ms for declared endpoint query classes;
- node-agent operation receipt success above 99.9% excluding denied requests;
- automatic rollback after failed boot acceptance within two boot attempts;
- no loss of committed critical Orgo work under one abrupt power interruption after storage flush guarantees;
- quarterly successful Sovereignty Bundle restore for critical tenants.

## 3. Error budgets

An error budget applies to the capability. Repeated safe denials caused by invalid artifacts are not availability failures, but unexplained denials or inability to inspect reason codes are.

## 4. Health endpoints

Health outputs are authenticated according to sensitivity. Public endpoints expose minimal status. Detailed dependency, tenant, and security state is restricted.

## 5. Synthetic tests

Nodes SHOULD periodically test active pack queries, policy vectors, publication-gateway redaction, local queue durability, and recovery prerequisites without mutating production truth.
