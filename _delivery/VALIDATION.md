# B-0032 — Rapport de validation

## Identité

- Branche : `bundle/b-0032-resource-governor-adaptateurs-et-persistance`
- Commit de base : `bee64f863215edfafd15522c9d3ed0778111dac0`
- Commit livré : `a086a4fb490303695759e15953bae93295c1d656`
- Sujet : `B-0032: Resource Governor — Adaptateurs et persistance`
- État Git après commit : propre

## Résumé de l’implémentation

Le bundle fournit six adaptateurs Resource Governor et la politique de migration associée :

- sonde procfs limitée aux métriques CPU, mémoire, I/O, processus et descripteurs;
- sonde systemd en lecture seule via des propriétés publiques et `systemctl show` sans shell;
- fournisseur de profil et d’enveloppes JSON confiné à des chemins explicitement configurés;
- client Node Agent utilisant uniquement `execute_node_operation` et un identifiant d’opération fourni par le profil;
- client Audit Broker exigeant un reçu terminal pour les transitions critiques;
- horloge UTC RFC 3339;
- documentation expliquant pourquoi aucune migration SQL n’est inventée dans cette révision.

Les observations n’inspectent ni `cmdline`, ni `environ`, ni mémoire de processus, ni contenu métier. Les métriques indisponibles sont omises plutôt que rapportées comme zéro.

## Fichiers livrés

- `components/resource-governor/migrations/README.md`
- `components/resource-governor/src/koa_resource_governor/adapters/__init__.py`
- `components/resource-governor/src/koa_resource_governor/adapters/audit_client.py`
- `components/resource-governor/src/koa_resource_governor/adapters/node_agent_client.py`
- `components/resource-governor/src/koa_resource_governor/adapters/proc_usage_probe.py`
- `components/resource-governor/src/koa_resource_governor/adapters/profile_file_provider.py`
- `components/resource-governor/src/koa_resource_governor/adapters/system_clock.py`
- `components/resource-governor/src/koa_resource_governor/adapters/systemd_usage_probe.py`

## Validations exécutées

| Commande ou contrôle | Code | Résultat |
|---|---:|---|
| `python -m compileall -q components/resource-governor/src` | 0 | pass |
| `PYTHONPATH=components/resource-governor/src python -m pytest -q /tmp/test_b0032.py` | 0 | 6 passed |
| `ProcUsageProbe(SystemClock()).observe(...) on the validation process` | 0 | pass; cpu, io, memory and process dimensions observed |
| `SystemctlPropertyReader with an isolated fake systemctl executable` | 0 | pass |
| `python docs/tools/check_greenfield_architecture.py` | 0 | pass |
| `python docs/tools/check_canonical_ownership.py` | 0 | pass |
| `python docs/tools/check_component_boundaries.py` | 0 | pass |
| `python docs/tools/check_generated_content.py` | 0 | pass |
| `python docs/tools/check_no_unresolved_state.py` | 0 | pass |
| `python docs/tools/check_security_architecture.py` | 0 | pass; controls=48, profiles=10, invariants=8 |
| `python docs/tools/check_artifact_contracts.py` | 0 | pass; schemas=37 |
| `python docs/tools/check_interfile_locks.py` | 0 | pass; referenced=165 |
| `python docs/tools/validate_docs.py` | 0 | pass; reserved subsystem mounts emitted non-blocking warnings |
| `git diff --check / git diff --cached --check` | 0 | pass |
| `closed file allowlist and standard-library-only import AST check` | 0 | pass |

## Dépendances et limites

### B-0017 — Bindings Python communs

Absent de la base fournie : `interfaces/python/` n’existe pas. Les adaptateurs utilisent donc uniquement la bibliothèque standard et des protocoles structurels locaux. L’alignement avec les bindings exacts reste à vérifier après intégration.

### B-0031 — Application et ports Resource Governor

Absent de la base fournie : `components/resource-governor/src/koa_resource_governor/ports/` n’existe pas. Les noms port-friendly (`observe_usage`, `apply_resource_control`, `load_profile`, `load_envelope`, `record`) sont fournis, mais les signatures finales doivent être contrôlées contre B-0031.

### Frontière Node Agent

Les documents Resource Governor autorisent un Node Agent ou un adaptateur de profil pour appliquer les contrôles hôte. Cependant, le catalogue fermé actuel de `koa-node-agent.component.json` ne contient pas d’opération de contrôle de ressources. Le client n’en invente donc aucune : `operation_id` est obligatoire et doit provenir du profil ou d’un contrat Node Agent ultérieurement accepté. Cette partie reste bloquée jusqu’à l’existence de cette opération déclarée.

### Persistance

L’inventaire du bundle ne contient aucun fichier SQL. Le README de migrations documente explicitement que les profils/enveloppes sont lus en mode immuable, les observations sont éphémères et les preuves sont déléguées à Audit Broker. Un futur stockage autoritaire Resource Governor devra arriver dans un bundle inventorié avec migrations, sauvegarde, restauration et réconciliation.

## Bundles débloqués

Aucun. Les dépendances B-0017 et B-0031 doivent être intégrées et validées, puis la frontière Node Agent doit exposer une opération fermée compatible.

## Diff stat

```text
a086a4f B-0032: Resource Governor — Adaptateurs et persistance
 components/resource-governor/migrations/README.md  |  26 +++
 .../src/koa_resource_governor/adapters/__init__.py |  57 +++++
 .../koa_resource_governor/adapters/audit_client.py | 127 +++++++++++
 .../adapters/node_agent_client.py                  | 235 +++++++++++++++++++++
 .../adapters/proc_usage_probe.py                   | 228 ++++++++++++++++++++
 .../adapters/profile_file_provider.py              | 216 +++++++++++++++++++
 .../koa_resource_governor/adapters/system_clock.py |  19 ++
 .../adapters/systemd_usage_probe.py                | 214 +++++++++++++++++++
 8 files changed, 1122 insertions(+)
 create mode 100644 components/resource-governor/migrations/README.md
 create mode 100644 components/resource-governor/src/koa_resource_governor/adapters/__init__.py
 create mode 100644 components/resource-governor/src/koa_resource_governor/adapters/audit_client.py
 create mode 100644 components/resource-governor/src/koa_resource_governor/adapters/node_agent_client.py
 create mode 100644 components/resource-governor/src/koa_resource_governor/adapters/proc_usage_probe.py
 create mode 100644 components/resource-governor/src/koa_resource_governor/adapters/profile_file_provider.py
 create mode 100644 components/resource-governor/src/koa_resource_governor/adapters/system_clock.py
 create mode 100644 components/resource-governor/src/koa_resource_governor/adapters/systemd_usage_probe.py
```

## Preuves jointes

- `MANIFEST.json` contient les empreintes SHA-256 de chaque fichier.
- `logs/` contient les sorties capturées des validations principales.
- `test_b0032.py` est le harnais externe de tests ciblés; il ne fait pas partie du commit.
