# Service Updates

## 1. Packaging

Services are distributed as signed OCI images referenced by digest. Tags are convenience pointers and MUST NOT be the sole activation identity.

## 2. Service Bundle

A Service Bundle manifest declares:

- image digests;
- Quadlet/unit versions;
- configuration schema versions;
- required secrets by reference, not value;
- database migration set;
- network and storage requirements;
- health checks;
- resource limits;
- compatible OS and policy versions.

## 3. Rootless execution

Application containers SHOULD run rootless under dedicated service identities. Images SHOULD be read-only, use explicit writable volumes, drop capabilities, and have bounded resources.

## 4. Deployment strategies

- **recreate**: acceptable for non-critical or local services with bounded downtime;
- **blue/green**: preferred when parallel validation is possible;
- **canary**: allowed only with observability and rollback thresholds;
- **rolling**: allowed on multi-node hubs when schema compatibility is proven.

## 5. Health and acceptance

A running process is not sufficient. Acceptance checks include domain API readiness, dependency health, policy connectivity, database compatibility, and representative contract tests.

## 6. Rollback

Rollback MUST account for data migrations and emitted events. If a schema or event cannot be reversed safely, the release MUST use forward repair or a superseding service bundle rather than pretending rollback is complete.

## 7. Supply-chain controls

Images SHOULD be minimal, pinned, scanned, SBOM-producing, provenance-attested, and rebuilt regularly from maintained bases. Runtime installation of packages is prohibited in production images.
