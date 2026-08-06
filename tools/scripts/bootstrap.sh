#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: tools/scripts/bootstrap.sh [--offline]

Validate the locked Python workspace and synchronize its local .venv with UV.
UV and Python must already be supplied by the active development profile.
EOF
}

fail() {
  printf 'bootstrap: error: %s\n' "$1" >&2
  exit 69
}

offline=0
while (($#)); do
  case "$1" in
    --offline) offline=1 ;;
    -h|--help) usage; exit 0 ;;
    *) printf 'bootstrap: error: unknown argument: %s\n' "$1" >&2; usage >&2; exit 2 ;;
  esac
  shift
done

script_dir="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
repository_root="$(CDPATH= cd -- "${script_dir}/../.." && pwd)"

for marker in pyproject.toml uv.lock .python-version; do
  [[ -f "${repository_root}/${marker}" ]] || fail "missing required workspace marker: ${marker}"
done

command -v python >/dev/null 2>&1 || fail "python is not available from the active profile"
command -v uv >/dev/null 2>&1 || fail "uv is not available from the active profile"

cd -- "${repository_root}"
printf 'bootstrap: repository root: %s\n' "${repository_root}"
printf 'bootstrap: verifying uv.lock\n'
uv lock --check

printf 'bootstrap: synchronizing .venv from frozen inputs%s\n' "$([[ ${offline} -eq 1 ]] && printf ' (offline)' || true)"
if [[ ${offline} -eq 1 ]]; then
  UV_OFFLINE=1 uv sync --frozen --all-groups
else
  uv sync --frozen --all-groups
fi

printf 'bootstrap: complete\n'
