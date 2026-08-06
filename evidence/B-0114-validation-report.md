# B-0114 — Rapport de validation

## Statut

**Implémentation validée isolément, intégration bloquée.**

Les six fichiers autorisés ont été créés et validés. Les dépendances B-0107 et B-0108, le workspace Python racine et les scripts locaux des suites contrats/composants ne sont pas présents dans les artefacts montés. Les workflows hébergés n'ont donc pas été exécutés de bout en bout.

## Résultat fonctionnel

- trois identités de checks requises et stables;
- trois workflows minces, à permissions `contents: read`;
- aucune utilisation de `pull_request_target`, secret ou permission d'écriture;
- synchronisation exacte `uv sync --frozen --all-groups`;
- commandes locales identiques à celles appelées par les workflows;
- aucun filtre `on.paths`, afin que les checks requis soient toujours émis;
- routage de chemins avec repli `run_all`;
- couverture explicite des 1 040 chemins et 35 racines de l'architecture gelée.

## Fichiers

- `.github/workflows/components.yml`
- `.github/workflows/contracts.yml`
- `.github/workflows/documentation.yml`
- `ci/README.md`
- `ci/policies/path-filters.json`
- `ci/policies/required-checks.json`

## Validations réussies

- validation structurelle B-0114;
- parse JSON avec `jq`;
- parse YAML avec détection externe de structure et clés stables;
- `check_greenfield_architecture.py`;
- `check_canonical_ownership.py`;
- `check_component_boundaries.py`;
- `check_generated_content.py`;
- `check_traceability.py`;
- `check_no_unresolved_state.py`;
- `validate_docs.py`;
- `git diff --cached --check`;
- application du patch dans un dépôt vide;
- comparaison SHA-256 des six fichiers après application.

## Limites

Les commandes suivantes sont déclarées mais n'ont pas pu être exécutées dans le dépôt complet absent:

```text
uv sync --frozen --all-groups
uv run --frozen python ci/scripts/run-contracts.py
uv run --frozen python ci/scripts/run-components.py
```

La commande documentaire sous-jacente `python docs/tools/validate_docs.py` a été exécutée directement et a réussi. L'action GitHub hébergée, `actions/checkout@v4`, `astral-sh/setup-uv@v6` et le runner `ubuntu-24.04` n'ont pas été exécutés dans cet environnement local.

## Commit

- Branche: `bundle/b-0114-politiques-ci-et-workflows-documentaires-contrats-composants`
- Commit: `9b63eaff3bc49a7b8bec90707516cd173865e085`
- Message: `B-0114: Politiques CI et workflows documentaires/contrats/composants`

## Diff stat

```text
.github/workflows/components.yml    |  38 ++++++
 .github/workflows/contracts.yml     |  38 ++++++
 .github/workflows/documentation.yml |  38 ++++++
 ci/README.md                        |  65 +++++++++
 ci/policies/path-filters.json       | 266 ++++++++++++++++++++++++++++++++++++
 ci/policies/required-checks.json    | 118 ++++++++++++++++
 6 files changed, 563 insertions(+)
```
