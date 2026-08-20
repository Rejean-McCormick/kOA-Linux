from __future__ import annotations

from io import StringIO
from importlib import import_module
from inspect import Parameter, signature
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace
from unittest.mock import patch

import pytest

TOOLS_SRC = Path(__file__).resolve().parents[1] / "src"
if str(TOOLS_SRC) not in sys.path:
    sys.path.insert(0, str(TOOLS_SRC))

from koa_tools import __version__  # noqa: E402
from koa_tools import cli  # noqa: E402
from koa_tools.process import (  # noqa: E402
    ProcessExecutionError,
    run_process,
)


def _workspace(tmp_path: Path) -> Path:
    for marker in cli.ROOT_MARKERS:
        (tmp_path / marker).write_text("\n", encoding="utf-8")
    return tmp_path


def _invoke(arguments: list[str], *, start_directory: Path | None = None):
    stdout = StringIO()
    stderr = StringIO()
    code = cli.main(
        arguments,
        stdout=stdout,
        stderr=stderr,
        start_directory=start_directory,
    )
    return code, stdout.getvalue(), stderr.getvalue()


def test_help_is_stable_and_lists_closed_catalog() -> None:
    first = _invoke(["--help"])
    second = _invoke([])

    assert first == second
    code, stdout, stderr = first
    assert code == cli.ExitCode.OK
    assert stderr == ""
    for command in cli.COMMANDS:
        assert command.name in stdout
    assert "Root options must precede the command" in stdout


def test_version_is_explicit() -> None:
    code, stdout, stderr = _invoke(["--version"])

    assert code == cli.ExitCode.OK
    assert stdout == f"koa-tools {__version__}\n"
    assert stderr == ""


def test_unknown_command_is_a_usage_error() -> None:
    code, stdout, stderr = _invoke(["not-a-command"])

    assert code == cli.ExitCode.USAGE
    assert stdout == ""
    assert "invalid choice" in stderr
    assert "Try 'koa --help' for usage." in stderr


def test_missing_repository_root_fails_explicitly(tmp_path: Path) -> None:
    code, stdout, stderr = _invoke(["validate"], start_directory=tmp_path)

    assert code == cli.ExitCode.UNAVAILABLE
    assert stdout == ""
    assert "no repository root found" in stderr
    assert "pyproject.toml, uv.lock, .python-version" in stderr


def test_missing_command_module_fails_explicitly(tmp_path: Path) -> None:
    root = _workspace(tmp_path)
    missing = ModuleNotFoundError("catalogued command module is absent")
    missing.name = "koa_tools.commands.validate"

    with patch.object(cli, "import_module", side_effect=missing):
        code, stdout, stderr = _invoke(["validate"], start_directory=root)

    assert code == cli.ExitCode.UNAVAILABLE
    assert stdout == ""
    assert "is catalogued but its module" in stderr
    assert "not present in this source revision" in stderr


def test_dispatch_passes_only_command_arguments_and_resolved_root(tmp_path: Path) -> None:
    root = _workspace(tmp_path)
    observed: dict[str, object] = {}

    def command_main(argv: tuple[str, ...], *, repository_root: Path) -> int:
        observed["argv"] = argv
        observed["repository_root"] = repository_root
        return 7

    fake_module = SimpleNamespace(main=command_main)
    with patch.object(cli, "_load_command", return_value=fake_module):
        code, stdout, stderr = _invoke(
            ["--repository-root", str(root), "validate", "--strict", "item"],
            start_directory=root.parent,
        )

    assert code == 7
    assert stdout == ""
    assert stderr == ""
    assert observed == {
        "argv": ("--strict", "item"),
        "repository_root": root.resolve(),
    }


@pytest.mark.parametrize("spec", cli.COMMANDS, ids=lambda spec: spec.name)
def test_catalogued_command_main_accepts_resolved_repository_root(spec: cli.CommandSpec) -> None:
    module = import_module(spec.module)
    handler = getattr(module, "main")
    parameter = signature(handler).parameters.get("repository_root")

    assert parameter is not None
    assert parameter.kind is Parameter.KEYWORD_ONLY


@pytest.mark.parametrize("spec", cli.COMMANDS, ids=lambda spec: spec.name)
def test_catalogued_command_help_dispatches_through_root_cli(
    spec: cli.CommandSpec,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    root = _workspace(tmp_path)

    code, stdout, stderr = _invoke(
        ["--repository-root", str(root), spec.name, "--help"],
        start_directory=root.parent,
    )
    captured = capsys.readouterr()

    assert code == cli.ExitCode.OK
    assert stdout == ""
    assert stderr == ""
    assert captured.err == ""
    assert "usage:" in captured.out


def test_non_integer_command_result_is_a_software_error(tmp_path: Path) -> None:
    root = _workspace(tmp_path)
    fake_module = SimpleNamespace(main=lambda argv, repository_root: None)

    with patch.object(cli, "_load_command", return_value=fake_module):
        code, stdout, stderr = _invoke(["validate"], start_directory=root)

    assert code == cli.ExitCode.SOFTWARE
    assert stdout == ""
    assert "an integer exit code is required" in stderr


def test_process_runner_captures_output_without_shell(tmp_path: Path) -> None:
    result = run_process(
        [sys.executable, "-c", "print('stable-output')"],
        cwd=tmp_path,
    )

    assert result.succeeded
    assert result.cwd == tmp_path.resolve()
    assert result.stdout == "stable-output\n"
    assert result.stderr == ""
    assert result.argv[0] == sys.executable


def test_process_runner_rejects_shell_command_string() -> None:
    with pytest.raises(TypeError, match="not a shell command"):
        run_process("python -c pass")  # type: ignore[arg-type]


def test_process_runner_exposes_nonzero_result(tmp_path: Path) -> None:
    with pytest.raises(ProcessExecutionError) as captured:
        run_process(
            [sys.executable, "-c", "import sys; print('failure'); sys.exit(4)"],
            cwd=tmp_path,
        )

    assert captured.value.result.returncode == 4
    assert captured.value.result.stdout == "failure\n"


def test_cli_module_is_directly_executable() -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "koa_tools.cli", "--help"],
        cwd=TOOLS_SRC,
        env={
            "PATH": str(Path(sys.executable).parent),
            "PYTHONDONTWRITEBYTECODE": "1",
        },
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0
    assert completed.stderr == ""
    assert completed.stdout.startswith("usage: koa")


def _write_executable(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")
    path.chmod(0o755)


def _script_fixture(tmp_path: Path) -> tuple[Path, Path]:
    repository = tmp_path / "repository"
    scripts = repository / "tools" / "scripts"
    scripts.mkdir(parents=True)
    source_scripts = Path(__file__).resolve().parents[1] / "scripts"
    for name in ("bootstrap.sh", "setup-development.sh"):
        target = scripts / name
        target.write_text((source_scripts / name).read_text(encoding="utf-8"), encoding="utf-8")
        target.chmod(0o755)

    for marker in (*cli.ROOT_MARKERS, ".pre-commit-config.yaml"):
        (repository / marker).write_text("\n", encoding="utf-8")

    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    log = tmp_path / "commands.log"
    _write_executable(
        fake_bin / "uv",
        "#!/usr/bin/env bash\nprintf 'uv:%s\\n' \"$*\" >> \"$KOA_TEST_LOG\"\nexit 0\n",
    )
    _write_executable(fake_bin / "python", "#!/usr/bin/env bash\nexit 0\n")
    _write_executable(
        fake_bin / "git",
        "#!/usr/bin/env bash\nprintf 'true\\n'\nexit 0\n",
    )
    return repository, log


def test_bootstrap_shell_is_idempotent(tmp_path: Path) -> None:
    if sys.platform == "win32":
        pytest.skip("POSIX shell validation")
    repository, log = _script_fixture(tmp_path)
    script = repository / "tools" / "scripts" / "bootstrap.sh"
    environment = {
        "PATH": f"{tmp_path / 'bin'}:/usr/bin:/bin",
        "KOA_TEST_LOG": str(log),
    }

    first = subprocess.run(
        [str(script), "--offline"],
        cwd=repository,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )
    second = subprocess.run(
        [str(script), "--offline"],
        cwd=repository,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )

    assert first.returncode == second.returncode == 0
    assert first.stdout == second.stdout
    assert first.stderr == second.stderr == ""
    assert log.read_text(encoding="utf-8").splitlines() == [
        "uv:lock --check",
        "uv:sync --frozen --all-groups",
        "uv:lock --check",
        "uv:sync --frozen --all-groups",
    ]


def test_setup_development_shell_is_idempotent(tmp_path: Path) -> None:
    if sys.platform == "win32":
        pytest.skip("POSIX shell validation")
    repository, log = _script_fixture(tmp_path)
    script = repository / "tools" / "scripts" / "setup-development.sh"
    environment = {
        "PATH": f"{tmp_path / 'bin'}:/usr/bin:/bin",
        "KOA_TEST_LOG": str(log),
    }

    results = [
        subprocess.run(
            [str(script)],
            cwd=repository,
            env=environment,
            capture_output=True,
            text=True,
            check=False,
        )
        for _ in range(2)
    ]

    assert [result.returncode for result in results] == [0, 0]
    assert results[0].stdout == results[1].stdout
    assert results[0].stderr == results[1].stderr == ""
    assert log.read_text(encoding="utf-8").splitlines() == [
        "uv:lock --check",
        "uv:sync --frozen --all-groups",
        "uv:run --frozen pre-commit install",
        "uv:run --frozen python -m koa_tools.cli --help",
        "uv:lock --check",
        "uv:sync --frozen --all-groups",
        "uv:run --frozen pre-commit install",
        "uv:run --frozen python -m koa_tools.cli --help",
    ]


def test_powershell_scripts_preserve_locked_command_contract() -> None:
    scripts = Path(__file__).resolve().parents[1] / "scripts"
    bootstrap = (scripts / "bootstrap.ps1").read_text(encoding="utf-8")
    setup = (scripts / "setup-development.ps1").read_text(encoding="utf-8")

    for marker in cli.ROOT_MARKERS:
        assert marker in bootstrap
    assert "@('lock', '--check')" in bootstrap
    assert "@('sync', '--frozen', '--all-groups')" in bootstrap
    assert "UV_OFFLINE" in bootstrap
    assert "pre-commit', 'install'" in setup
    assert "python', '-m', 'koa_tools.cli', '--help'" in setup
