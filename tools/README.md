# kOA repository tooling

`tools/` contains the local, non-privileged command surface used to validate,
generate, assemble, test, diagnose, build, verify, and release declared kOA
artifacts. It orchestrates canonical implementations; it does not own component
policy, profile composition, release authority, or privileged host operations.

The source layout and path ownership are defined by:

- `docs/02-system/code-and-filesystem-architecture/31-operations-tests-tools-development-and-ci.md`;
- `docs/02-system/code-and-filesystem-architecture/33-path-ownership-and-change-rules.md`;
- `docs/contracts/toolchains/python-uv.toolchain.json`;
- `docs/05-development/14-build-test-and-validation.md`.

## Prerequisites

The active development profile must provide `python`, `uv`, and `git`. The
workspace root must already contain the version-controlled files
`pyproject.toml`, `uv.lock`, `.python-version`, and `.pre-commit-config.yaml`.
The scripts never download or install UV through a remote shell script and
never refresh dependency resolution implicitly.

Each branch or worktree owns its own `.venv`. A content-addressed UV download
cache may be shared, but a mutable installed environment must not be shared.

## Bootstrap

Linux or WSL:

```console
./tools/scripts/bootstrap.sh
./tools/scripts/bootstrap.sh --offline
```

PowerShell:

```powershell
./tools/scripts/bootstrap.ps1
./tools/scripts/bootstrap.ps1 -Offline
```

Bootstrap is idempotent. It performs exactly these locked operations:

1. verify `pyproject.toml`, `uv.lock`, and `.python-version`;
2. require profile-provided `python` and `uv`;
3. run `uv lock --check`;
4. run `uv sync --frozen --all-groups`, with `UV_OFFLINE=1` in offline mode.

An unavailable prerequisite or missing workspace marker exits explicitly. The
script does not repair a lock, select an undeclared index, or fall back to a
global Python environment.

## Development setup

Linux or WSL:

```console
./tools/scripts/setup-development.sh
```

PowerShell:

```powershell
./tools/scripts/setup-development.ps1
```

The setup script runs bootstrap, installs the repository-local pre-commit hook
through the frozen UV environment, and verifies the CLI help surface. Repeated
execution updates the same hook and synchronized environment rather than
creating parallel mutable state.

## Root CLI

The package entry point is `koa_tools.cli:main`. Until the root project exposes
the console script, the equivalent source invocation is:

```console
uv run --frozen python -m koa_tools.cli --help
```

The root help and command catalog are stable and do not import command modules.
The closed catalog is:

- `validate`;
- `generate`;
- `assemble`;
- `build-image`;
- `build-bundle`;
- `verify`;
- `test`;
- `release`;
- `diagnose`.

Root options must precede the command. `--repository-root PATH` may select an
explicit workspace root; otherwise the CLI searches upward from the current
working directory for all three canonical Python root markers.

A command module must expose this interface:

```text
main(argv: tuple[str, ...], *, repository_root: Path) -> int
```

Command modules return an integer exit code from 0 through 255. A catalogued
command whose implementation is absent exits with code 69. Invalid root CLI
arguments exit with code 2, an unexpected software defect exits with code 70,
and an interrupted command exits with code 130. No missing command is reported
as successful.

## Process execution API

`koa_tools.process.run_process` executes an argument vector without a shell,
uses a declared working directory, captures UTF-8 output, supports bounded
execution, and raises typed exceptions for start, timeout, and non-zero-exit
failures.

```python
from koa_tools.process import run_process

result = run_process(
    ["uv", "lock", "--check"],
    cwd=repository_root,
    timeout=120,
)
```

Do not pass secrets in command-line arguments. Secrets must enter a child
process only through an approved injected environment or broker. The process
API does not log environment values.

## Focused validation

From a synchronized workspace:

```console
uv run --frozen python -m compileall tools/src/koa_tools
uv run --frozen pytest tools/tests/test_cli.py
bash -n tools/scripts/bootstrap.sh tools/scripts/setup-development.sh
python docs/tools/check_greenfield_architecture.py
python docs/tools/validate_docs.py
```

Local success is workspace feedback, not release-authoritative evidence.
