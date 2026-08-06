#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: tools/scripts/setup-development.sh [--offline]

Bootstrap the locked workspace, install repository-local pre-commit hooks, and
verify that the kOA tooling CLI can display its stable help output.
EOF
}

fail() {
  printf 'setup-development: error: %s\n' "$1" >&2
  exit 69
}

offline=0
while (($#)); do
  case "$1" in
    --offline) offline=1 ;;
    -h|--help) usage; exit 0 ;;
    *) printf 'setup-development: error: unknown argument: %s\n' "$1" >&2; usage >&2; exit 2 ;;
  esac
  shift
done

script_dir="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
repository_root="$(CDPATH= cd -- "${script_dir}/../.." && pwd)"
bootstrap_args=()
if [[ ${offline} -eq 1 ]]; then
  bootstrap_args+=(--offline)
fi
"${script_dir}/bootstrap.sh" "${bootstrap_args[@]}"

cd -- "${repository_root}"
command -v git >/dev/null 2>&1 || fail "git is required to configure development hooks"
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || fail "repository root is not a Git worktree"
[[ -f .pre-commit-config.yaml ]] || fail "missing .pre-commit-config.yaml"

printf 'setup-development: installing repository-local pre-commit hook\n'
uv run --frozen pre-commit install

printf 'setup-development: verifying CLI help\n'
uv run --frozen python -m koa_tools.cli --help >/dev/null
printf 'setup-development: complete\n'
