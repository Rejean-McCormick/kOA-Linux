#!/usr/bin/env python3
"""Check that a kOA documentation repository is clean and publishable.

The checker detects repository debris, unsafe filesystem objects, local reports,
editor backups, runtime caches, build outputs, high-confidence secret material,
unexpected binaries, and Git working-tree changes when Git is available.

Typical usage:

    uv run python docs/tools/check_clean_repository.py
    uv run python docs/tools/check_clean_repository.py --partial
    uv run python docs/tools/check_clean_repository.py \
        --report-json build/clean-repository-report.json
    uv run python docs/tools/check_clean_repository.py --self-test

Strict mode is intended for release gates and documentation cutover. Partial
mode keeps unsafe-file and secret checks strict while reporting ordinary
working-tree changes and missing optional repository metadata as warnings.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import fnmatch
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import textwrap
from typing import Any, Iterable, Iterator, Mapping, Sequence


EXIT_OK = 0
EXIT_VALIDATION_ERROR = 1

DEFAULT_MAX_FILE_BYTES = 10 * 1024 * 1024
DEFAULT_SECRET_SCAN_BYTES = 2 * 1024 * 1024

TEXT_SUFFIXES = {
    ".md",
    ".json",
    ".yaml",
    ".yml",
    ".py",
    ".toml",
    ".ini",
    ".cfg",
    ".conf",
    ".txt",
    ".csv",
    ".tsv",
    ".sh",
    ".bash",
    ".zsh",
    ".fish",
    ".ps1",
    ".service",
    ".socket",
    ".target",
    ".timer",
    ".path",
}

FORBIDDEN_BASENAMES = {
    ".DS_Store",
    "Thumbs.db",
    "ehthumbs.db",
    "desktop.ini",
    "Icon\r",
    ".directory",
    ".coverage",
    ".python-version.tmp",
}

FORBIDDEN_DIRECTORY_NAMES = {
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".hypothesis",
    ".tox",
    ".nox",
    ".cache",
    ".ipynb_checkpoints",
    "htmlcov",
}

FORBIDDEN_PATH_PATTERNS = (
    "*.swp",
    "*.swo",
    "*.swn",
    "*~",
    ".#*",
    "#*#",
    "*.bak",
    "*.backup",
    "*.orig",
    "*.rej",
    "*.tmp",
    "*.temp",
    "*.part",
    "*.download",
    "*.crdownload",
    "*.pyc",
    "*.pyo",
    "*.prof",
    "*.trace",
    "*.stackdump",
    "*.core",
    "core.*",
)

DOCS_LOCAL_OUTPUT_PATTERNS = (
    "docs/tools/*.report.json",
    "docs/tools/*-report.json",
    "docs/tools/*.log",
    "docs/tools/*.out",
    "docs/tools/*.err",
    "docs/**/validation-report.json",
    "docs/**/partial-report.json",
    "docs/**/.coverage",
    "docs/**/coverage.xml",
    "docs/**/junit.xml",
    "docs/build/**",
    "docs/dist/**",
    "docs/.cache/**",
)

UNEXPECTED_BINARY_SUFFIXES = {
    ".exe",
    ".dll",
    ".so",
    ".dylib",
    ".a",
    ".o",
    ".obj",
    ".class",
    ".jar",
    ".war",
    ".bin",
    ".dat",
    ".dmp",
    ".iso",
    ".img",
    ".qcow2",
    ".vmdk",
}

ARCHIVE_SUFFIXES = {
    ".zip",
    ".tar",
    ".tgz",
    ".gz",
    ".bz2",
    ".xz",
    ".7z",
    ".rar",
}

ALLOWED_EMPTY_BASENAMES = {
    ".gitkeep",
    ".keep",
}

HIGH_CONFIDENCE_SECRET_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "private_key",
        re.compile(
            r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----"
        ),
    ),
    (
        "aws_access_key",
        re.compile(r"(?<![A-Z0-9])AKIA[0-9A-Z]{16}(?![A-Z0-9])"),
    ),
    (
        "github_classic_token",
        re.compile(r"(?<![A-Za-z0-9_])gh[opusr]_[A-Za-z0-9]{36,255}"),
    ),
    (
        "github_fine_grained_token",
        re.compile(r"(?<![A-Za-z0-9_])github_pat_[A-Za-z0-9_]{60,255}"),
    ),
    (
        "slack_token",
        re.compile(r"(?<![A-Za-z0-9-])xox[baprs]-[A-Za-z0-9-]{20,255}"),
    ),
    (
        "stripe_live_secret",
        re.compile(r"(?<![A-Za-z0-9_])sk_live_[A-Za-z0-9]{20,255}"),
    ),
    (
        "google_api_key",
        re.compile(r"(?<![A-Za-z0-9_-])AIza[0-9A-Za-z_-]{35}(?![A-Za-z0-9_-])"),
    ),
    (
        "jwt_bearer",
        re.compile(
            r"(?<![A-Za-z0-9_-])eyJ[A-Za-z0-9_-]{10,}\."
            r"[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"
        ),
    ),
)

PROBABLE_CREDENTIAL_URI_RE = re.compile(
    r"\b(?:https?|postgres(?:ql)?|mysql|mongodb(?:\+srv)?|redis)://"
    r"[^/\s:@]+:[^/\s@]+@"
)

REDUCTION_MARKERS = (
    "<redacted>",
    "[redacted]",
    "example.invalid",
    "example.com",
    "changeme",
    "not-a-real",
    "dummy",
    "placeholder",
)

DEFAULT_IGNORE_PATTERNS = (
    ".git/**",
    ".git",
    ".venv/**",
    ".venv",
    "node_modules/**",
    "node_modules",
)

CONFIG_FILENAMES = (
    ".koa-clean-repository.json",
    "koa-clean-repository.json",
)


@dataclass(order=True)
class Diagnostic:
    """One repository-cleanliness finding."""

    sort_key: tuple[str, int, str] = field(init=False, repr=False)
    severity: str
    code: str
    message: str
    path: str = ""
    line: int = 0
    details: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        severity_order = {"error": "0", "warning": "1", "info": "2"}
        self.sort_key = (
            self.path,
            self.line,
            severity_order.get(self.severity, "9") + self.code,
        )

    def display(self) -> str:
        location = self.path
        if self.line:
            location = f"{location}:{self.line}" if location else f"line {self.line}"
        prefix = f"{self.severity.upper()} {self.code}"
        if location:
            return f"{prefix} {location}: {self.message}"
        return f"{prefix}: {self.message}"


@dataclass
class RepositoryConfig:
    """Optional repository-owned checker configuration."""

    ignore_patterns: tuple[str, ...] = ()
    allowed_paths: tuple[str, ...] = ()
    allowed_binary_patterns: tuple[str, ...] = ()
    allowed_archive_patterns: tuple[str, ...] = ()
    allowed_empty_patterns: tuple[str, ...] = ()
    allowed_secret_fixture_patterns: tuple[str, ...] = ()
    max_file_bytes: int = DEFAULT_MAX_FILE_BYTES
    secret_scan_bytes: int = DEFAULT_SECRET_SCAN_BYTES
    require_git: bool = False
    require_gitignore: bool = False


@dataclass
class Options:
    root: Path
    docs_root: Path
    partial: bool = False
    git_check: str = "auto"
    report_json: Path | None = None
    fail_on_warning: bool = False
    max_diagnostics: int = 500
    exclude: tuple[str, ...] = ()
    quiet: bool = False


@dataclass
class GitEntry:
    code: str
    path: str
    original_path: str | None = None
    staged: bool = False
    unstaged: bool = False
    untracked: bool = False
    ignored: bool = False
    unmerged: bool = False


@dataclass
class Result:
    root: str
    docs_root: str
    mode: str
    started_at: str
    completed_at: str
    files_checked: int
    directories_checked: int
    bytes_checked: int
    diagnostics: list[Diagnostic]
    git: dict[str, Any]
    categories: dict[str, int]

    @property
    def errors(self) -> int:
        return sum(item.severity == "error" for item in self.diagnostics)

    @property
    def warnings(self) -> int:
        return sum(item.severity == "warning" for item in self.diagnostics)

    @property
    def information(self) -> int:
        return sum(item.severity == "info" for item in self.diagnostics)

    @property
    def passed(self) -> bool:
        return self.errors == 0

    def to_json(self) -> dict[str, Any]:
        return {
            "validator": {
                "id": "koa-clean-repository-checker",
                "version": "1.0.0",
            },
            "root": self.root,
            "docs_root": self.docs_root,
            "mode": self.mode,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "summary": {
                "passed": self.passed,
                "files_checked": self.files_checked,
                "directories_checked": self.directories_checked,
                "bytes_checked": self.bytes_checked,
                "errors": self.errors,
                "warnings": self.warnings,
                "information": self.information,
                "categories": self.categories,
            },
            "git": self.git,
            "diagnostics": [
                {
                    key: value
                    for key, value in asdict(item).items()
                    if key != "sort_key" and value not in ("", 0, {}, None)
                }
                for item in sorted(self.diagnostics)
            ],
        }


def now_utc() -> str:
    return datetime.now(tz=timezone.utc).isoformat().replace("+00:00", "Z")


def infer_roots() -> tuple[Path, Path]:
    script = Path(__file__).resolve()
    if script.parent.name == "tools" and script.parent.parent.name == "docs":
        docs_root = script.parent.parent
        return docs_root.parent, docs_root
    docs_root = Path.cwd() / "docs"
    return Path.cwd(), docs_root


def relative(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def path_matches(path: str, patterns: Iterable[str]) -> bool:
    return any(fnmatch.fnmatch(path, pattern) for pattern in patterns)


def is_allowed(path: str, config: RepositoryConfig) -> bool:
    return path_matches(path, config.allowed_paths)


def add_diagnostic(
    diagnostics: list[Diagnostic],
    options: Options,
    severity: str,
    code: str,
    message: str,
    path: str = "",
    line: int = 0,
    details: dict[str, Any] | None = None,
) -> None:
    if len(diagnostics) >= options.max_diagnostics:
        return
    diagnostics.append(
        Diagnostic(
            severity=severity,
            code=code,
            message=message,
            path=path,
            line=line,
            details=details or {},
        )
    )


def strict_or_warning(options: Options) -> str:
    return "warning" if options.partial else "error"


def load_config(root: Path, diagnostics: list[Diagnostic], options: Options) -> RepositoryConfig:
    config_path = next(
        (root / name for name in CONFIG_FILENAMES if (root / name).exists()),
        None,
    )
    if config_path is None:
        return RepositoryConfig()

    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        add_diagnostic(
            diagnostics,
            options,
            "error",
            "KOA-CLEAN-CONFIG-001",
            f"unable to parse repository-cleanliness configuration: {exc}",
            config_path.name,
        )
        return RepositoryConfig()

    if not isinstance(data, dict):
        add_diagnostic(
            diagnostics,
            options,
            "error",
            "KOA-CLEAN-CONFIG-002",
            "repository-cleanliness configuration must be a JSON object",
            config_path.name,
        )
        return RepositoryConfig()

    allowed_keys = {
        "ignore_patterns",
        "allowed_paths",
        "allowed_binary_patterns",
        "allowed_archive_patterns",
        "allowed_empty_patterns",
        "allowed_secret_fixture_patterns",
        "max_file_bytes",
        "secret_scan_bytes",
        "require_git",
        "require_gitignore",
    }
    unknown = sorted(set(data) - allowed_keys)
    if unknown:
        add_diagnostic(
            diagnostics,
            options,
            "error",
            "KOA-CLEAN-CONFIG-003",
            "unknown configuration fields: " + ", ".join(unknown),
            config_path.name,
        )

    def strings(key: str) -> tuple[str, ...]:
        value = data.get(key, [])
        if not isinstance(value, list) or any(
            not isinstance(item, str) or not item for item in value
        ):
            add_diagnostic(
                diagnostics,
                options,
                "error",
                "KOA-CLEAN-CONFIG-004",
                f"{key} must be an array of non-empty strings",
                config_path.name,
            )
            return ()
        return tuple(value)

    def positive_int(key: str, default: int) -> int:
        value = data.get(key, default)
        if not isinstance(value, int) or isinstance(value, bool) or value < 1:
            add_diagnostic(
                diagnostics,
                options,
                "error",
                "KOA-CLEAN-CONFIG-005",
                f"{key} must be a positive integer",
                config_path.name,
            )
            return default
        return value

    def boolean(key: str, default: bool) -> bool:
        value = data.get(key, default)
        if not isinstance(value, bool):
            add_diagnostic(
                diagnostics,
                options,
                "error",
                "KOA-CLEAN-CONFIG-006",
                f"{key} must be boolean",
                config_path.name,
            )
            return default
        return value

    return RepositoryConfig(
        ignore_patterns=strings("ignore_patterns"),
        allowed_paths=strings("allowed_paths"),
        allowed_binary_patterns=strings("allowed_binary_patterns"),
        allowed_archive_patterns=strings("allowed_archive_patterns"),
        allowed_empty_patterns=strings("allowed_empty_patterns"),
        allowed_secret_fixture_patterns=strings(
            "allowed_secret_fixture_patterns"
        ),
        max_file_bytes=positive_int("max_file_bytes", DEFAULT_MAX_FILE_BYTES),
        secret_scan_bytes=positive_int(
            "secret_scan_bytes", DEFAULT_SECRET_SCAN_BYTES
        ),
        require_git=boolean("require_git", False),
        require_gitignore=boolean("require_gitignore", False),
    )


def should_ignore(path: str, options: Options, config: RepositoryConfig) -> bool:
    patterns = (
        *DEFAULT_IGNORE_PATTERNS,
        *options.exclude,
        *config.ignore_patterns,
    )
    return path_matches(path, patterns)


def discover_entries(
    options: Options,
    config: RepositoryConfig,
    diagnostics: list[Diagnostic],
) -> tuple[list[Path], list[Path]]:
    files: list[Path] = []
    directories: list[Path] = []

    for current_root, directory_names, file_names in os.walk(
        options.root,
        topdown=True,
        followlinks=False,
    ):
        current = Path(current_root)
        kept_directories: list[str] = []

        for name in sorted(directory_names):
            candidate = current / name
            try:
                rel = relative(candidate, options.root)
            except (OSError, ValueError):
                rel = candidate.name

            if should_ignore(rel, options, config):
                continue

            if candidate.is_symlink():
                validate_symlink(candidate, rel, diagnostics, options)
                continue

            directories.append(candidate)
            kept_directories.append(name)

        directory_names[:] = kept_directories

        for name in sorted(file_names):
            candidate = current / name
            try:
                rel = relative(candidate, options.root)
            except (OSError, ValueError):
                rel = candidate.name

            if should_ignore(rel, options, config):
                continue
            if candidate.is_symlink():
                validate_symlink(candidate, rel, diagnostics, options)
                continue
            files.append(candidate)

    return files, directories


def validate_symlink(
    path: Path,
    rel: str,
    diagnostics: list[Diagnostic],
    options: Options,
) -> None:
    try:
        target = path.resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        add_diagnostic(
            diagnostics,
            options,
            "error",
            "KOA-CLEAN-FS-001",
            f"broken or cyclic symbolic link: {exc}",
            rel,
        )
        return

    try:
        target.relative_to(options.root.resolve())
    except ValueError:
        add_diagnostic(
            diagnostics,
            options,
            "error",
            "KOA-CLEAN-FS-002",
            "symbolic link escapes the repository root",
            rel,
            details={"target": str(target)},
        )


def validate_directory(
    path: Path,
    rel: str,
    config: RepositoryConfig,
    diagnostics: list[Diagnostic],
    options: Options,
) -> None:
    if is_allowed(rel, config):
        return

    name = path.name
    if name in FORBIDDEN_DIRECTORY_NAMES:
        add_diagnostic(
            diagnostics,
            options,
            "error",
            "KOA-CLEAN-DIR-001",
            f"runtime or tool cache directory is not permitted: {name}",
            rel,
        )
    if rel.startswith("docs/") and name in {"build", "dist", "out", "reports"}:
        add_diagnostic(
            diagnostics,
            options,
            "error",
            "KOA-CLEAN-DIR-002",
            "local build or report directory is not permitted inside docs",
            rel,
        )


def validate_file_kind(
    path: Path,
    rel: str,
    config: RepositoryConfig,
    diagnostics: list[Diagnostic],
    options: Options,
) -> None:
    try:
        mode = path.lstat().st_mode
    except OSError as exc:
        add_diagnostic(
            diagnostics,
            options,
            "error",
            "KOA-CLEAN-FS-003",
            f"unable to inspect filesystem object: {exc}",
            rel,
        )
        return

    if stat.S_ISREG(mode):
        return
    if stat.S_ISFIFO(mode):
        kind = "FIFO"
    elif stat.S_ISSOCK(mode):
        kind = "socket"
    elif stat.S_ISCHR(mode):
        kind = "character device"
    elif stat.S_ISBLK(mode):
        kind = "block device"
    else:
        kind = "non-regular filesystem object"

    add_diagnostic(
        diagnostics,
        options,
        "error",
        "KOA-CLEAN-FS-004",
        f"{kind} is not permitted in the repository",
        rel,
    )


def validate_file_name(
    path: Path,
    rel: str,
    config: RepositoryConfig,
    diagnostics: list[Diagnostic],
    options: Options,
) -> None:
    if is_allowed(rel, config):
        return

    name = path.name
    if name in FORBIDDEN_BASENAMES:
        add_diagnostic(
            diagnostics,
            options,
            "error",
            "KOA-CLEAN-NAME-001",
            f"forbidden platform or tool artifact: {name}",
            rel,
        )

    if path_matches(name, FORBIDDEN_PATH_PATTERNS) or path_matches(
        rel, FORBIDDEN_PATH_PATTERNS
    ):
        add_diagnostic(
            diagnostics,
            options,
            "error",
            "KOA-CLEAN-NAME-002",
            "temporary, backup, editor, crash, or bytecode file is not permitted",
            rel,
        )

    if path_matches(rel, DOCS_LOCAL_OUTPUT_PATTERNS):
        add_diagnostic(
            diagnostics,
            options,
            "error",
            "KOA-CLEAN-NAME-003",
            "local validation output or report is not permitted inside docs",
            rel,
        )

    suffix = path.suffix.lower()
    if suffix in UNEXPECTED_BINARY_SUFFIXES and not path_matches(
        rel, config.allowed_binary_patterns
    ):
        add_diagnostic(
            diagnostics,
            options,
            "error",
            "KOA-CLEAN-BINARY-001",
            f"unexpected binary artifact type {suffix!r}",
            rel,
        )

    if suffix in ARCHIVE_SUFFIXES and rel.startswith("docs/") and not path_matches(
        rel, config.allowed_archive_patterns
    ):
        add_diagnostic(
            diagnostics,
            options,
            "error",
            "KOA-CLEAN-ARCHIVE-001",
            "archive is not permitted inside active documentation without an explicit allowance",
            rel,
        )

    lower_name = name.lower()
    if lower_name == ".env" or (
        lower_name.startswith(".env.")
        and not lower_name.endswith(
            (".example", ".sample", ".template", ".dist")
        )
    ):
        add_diagnostic(
            diagnostics,
            options,
            "error",
            "KOA-CLEAN-SECRET-001",
            "live environment file is not permitted in the repository",
            rel,
        )

    if suffix in {".pem", ".key", ".p12", ".pfx", ".jks", ".keystore"}:
        add_diagnostic(
            diagnostics,
            options,
            "error",
            "KOA-CLEAN-SECRET-002",
            f"credential or key container {suffix!r} is not permitted",
            rel,
        )


def validate_file_size(
    path: Path,
    rel: str,
    config: RepositoryConfig,
    diagnostics: list[Diagnostic],
    options: Options,
) -> int:
    try:
        size = path.stat().st_size
    except OSError as exc:
        add_diagnostic(
            diagnostics,
            options,
            "error",
            "KOA-CLEAN-FILE-001",
            f"unable to stat file: {exc}",
            rel,
        )
        return 0

    if size == 0 and path.name not in ALLOWED_EMPTY_BASENAMES and not path_matches(
        rel, config.allowed_empty_patterns
    ):
        add_diagnostic(
            diagnostics,
            options,
            "warning",
            "KOA-CLEAN-FILE-002",
            "empty file requires an explicit repository purpose",
            rel,
        )

    if size > config.max_file_bytes:
        add_diagnostic(
            diagnostics,
            options,
            "warning",
            "KOA-CLEAN-FILE-003",
            f"file exceeds the configured size threshold of {config.max_file_bytes} bytes",
            rel,
            details={"bytes": size},
        )
    return size


def is_probably_binary(path: Path, sample: bytes) -> bool:
    if path.suffix.lower() in TEXT_SUFFIXES:
        return False
    if b"\x00" in sample:
        return True
    if not sample:
        return False
    control = sum(
        byte < 9 or (13 < byte < 32)
        for byte in sample
    )
    return control / len(sample) > 0.05


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def looks_reduced(text: str, start: int, end: int) -> bool:
    window = text[max(0, start - 80) : min(len(text), end + 80)].casefold()
    return any(marker in window for marker in REDUCTION_MARKERS)


def scan_secrets(
    path: Path,
    rel: str,
    config: RepositoryConfig,
    diagnostics: list[Diagnostic],
    options: Options,
) -> None:
    if path_matches(rel, config.allowed_secret_fixture_patterns):
        return
    if PurePosixPath(rel).name in {"check_clean_repository.py", "check_development_isolation.py"}:
        return

    try:
        with path.open("rb") as stream:
            sample = stream.read(config.secret_scan_bytes)
    except OSError as exc:
        add_diagnostic(
            diagnostics,
            options,
            "error",
            "KOA-CLEAN-FILE-004",
            f"unable to read file for secret scan: {exc}",
            rel,
        )
        return

    if is_probably_binary(path, sample):
        return
    try:
        text = sample.decode("utf-8")
    except UnicodeDecodeError:
        add_diagnostic(
            diagnostics,
            options,
            "warning",
            "KOA-CLEAN-ENC-001",
            "text-like file is not valid UTF-8",
            rel,
        )
        return

    for secret_type, pattern in HIGH_CONFIDENCE_SECRET_PATTERNS:
        for match in pattern.finditer(text):
            if looks_reduced(text, match.start(), match.end()):
                continue
            add_diagnostic(
                diagnostics,
                options,
                "error",
                "KOA-CLEAN-SECRET-003",
                f"high-confidence {secret_type} pattern detected",
                rel,
                line_number(text, match.start()),
            )

    for match in PROBABLE_CREDENTIAL_URI_RE.finditer(text):
        if looks_reduced(text, match.start(), match.end()):
            continue
        add_diagnostic(
            diagnostics,
            options,
            "error",
            "KOA-CLEAN-SECRET-004",
            "URI appears to contain embedded credentials",
            rel,
            line_number(text, match.start()),
        )


def validate_permissions(
    path: Path,
    rel: str,
    diagnostics: list[Diagnostic],
    options: Options,
) -> None:
    if os.name == "nt":
        return
    try:
        mode = stat.S_IMODE(path.stat().st_mode)
    except OSError:
        return

    if mode & stat.S_IWOTH:
        add_diagnostic(
            diagnostics,
            options,
            "error",
            "KOA-CLEAN-PERM-001",
            "world-writable file is not permitted",
            rel,
            details={"mode": oct(mode)},
        )
    if mode & stat.S_ISUID or mode & stat.S_ISGID:
        add_diagnostic(
            diagnostics,
            options,
            "error",
            "KOA-CLEAN-PERM-002",
            "setuid or setgid file is not permitted",
            rel,
            details={"mode": oct(mode)},
        )


def validate_gitignore(
    root: Path,
    config: RepositoryConfig,
    diagnostics: list[Diagnostic],
    options: Options,
) -> None:
    gitignore = root / ".gitignore"
    if not gitignore.exists():
        if config.require_gitignore:
            add_diagnostic(
                diagnostics,
                options,
                strict_or_warning(options),
                "KOA-CLEAN-GITIGNORE-001",
                ".gitignore is required by repository configuration",
                ".gitignore",
            )
        return

    try:
        text = gitignore.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        add_diagnostic(
            diagnostics,
            options,
            "error",
            "KOA-CLEAN-GITIGNORE-002",
            f"unable to read .gitignore: {exc}",
            ".gitignore",
        )
        return

    recommended_groups = {
        "python_bytecode": ("__pycache__/", "*.py[cod]"),
        "python_venv": (".venv/",),
        "test_cache": (".pytest_cache/", ".mypy_cache/", ".ruff_cache/"),
        "editor_backup": ("*.swp", "*~"),
        "coverage": (".coverage", "htmlcov/"),
    }
    normalized = {
        line.strip()
        for line in text.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    missing_groups = [
        name
        for name, alternatives in recommended_groups.items()
        if not any(item in normalized for item in alternatives)
    ]
    if missing_groups:
        add_diagnostic(
            diagnostics,
            options,
            "warning",
            "KOA-CLEAN-GITIGNORE-003",
            "recommended ignore coverage is absent for: "
            + ", ".join(missing_groups),
            ".gitignore",
        )


def git_available() -> bool:
    return shutil.which("git") is not None


def git_repository_root(root: Path) -> Path | None:
    if not git_available():
        return None
    process = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "--show-toplevel"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if process.returncode != 0:
        return None
    value = process.stdout.strip()
    return Path(value).resolve() if value else None


def parse_git_status(raw: bytes) -> list[GitEntry]:
    entries: list[GitEntry] = []
    parts = raw.split(b"\0")
    index = 0

    while index < len(parts):
        part = parts[index]
        index += 1
        if not part:
            continue
        text = part.decode("utf-8", errors="replace")
        if len(text) < 3:
            continue

        code = text[:2]
        path = text[3:]
        original_path: str | None = None

        if "R" in code or "C" in code:
            if index < len(parts) and parts[index]:
                original_path = parts[index].decode("utf-8", errors="replace")
                index += 1

        entries.append(
            GitEntry(
                code=code,
                path=path,
                original_path=original_path,
                staged=code[0] not in {" ", "?"},
                unstaged=code[1] not in {" ", "?"},
                untracked=code == "??",
                ignored=code == "!!",
                unmerged="U" in code or code in {"AA", "DD"},
            )
        )
    return entries


def run_git(
    args: Sequence[str],
    root: Path,
) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def validate_git(
    options: Options,
    config: RepositoryConfig,
    diagnostics: list[Diagnostic],
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "mode": options.git_check,
        "available": git_available(),
        "repository": False,
        "entries": 0,
        "staged": 0,
        "unstaged": 0,
        "untracked": 0,
        "unmerged": 0,
        "tracked_forbidden": 0,
        "ignored_tracked": 0,
    }

    if options.git_check == "never":
        return result

    if not git_available():
        severity = (
            "error"
            if options.git_check == "always" or config.require_git
            else "warning"
        )
        add_diagnostic(
            diagnostics,
            options,
            severity,
            "KOA-CLEAN-GIT-001",
            "Git is unavailable; working-tree cleanliness cannot be verified",
        )
        return result

    repo_root = git_repository_root(options.root)
    if repo_root is None:
        severity = (
            "error"
            if options.git_check == "always" or config.require_git
            else "warning"
        )
        add_diagnostic(
            diagnostics,
            options,
            severity,
            "KOA-CLEAN-GIT-002",
            "repository root is not inside a Git work tree",
            str(options.root),
        )
        return result

    result["repository"] = True
    result["repository_root"] = str(repo_root)

    status_process = run_git(
        ["status", "--porcelain=v1", "-z", "--untracked-files=all"],
        repo_root,
    )
    if status_process.returncode != 0:
        add_diagnostic(
            diagnostics,
            options,
            "error",
            "KOA-CLEAN-GIT-003",
            "unable to read Git status",
            details={
                "stderr": status_process.stderr.decode(
                    "utf-8", errors="replace"
                )[-4000:]
            },
        )
        return result

    entries = parse_git_status(status_process.stdout)
    result["entries"] = len(entries)
    result["staged"] = sum(item.staged for item in entries)
    result["unstaged"] = sum(item.unstaged for item in entries)
    result["untracked"] = sum(item.untracked for item in entries)
    result["unmerged"] = sum(item.unmerged for item in entries)

    for entry in entries:
        if entry.unmerged:
            add_diagnostic(
                diagnostics,
                options,
                "error",
                "KOA-CLEAN-GIT-004",
                f"unmerged Git path with status {entry.code!r}",
                entry.path,
            )
            continue

        if entry.untracked:
            severity = strict_or_warning(options)
            message = "untracked path is present"
        elif entry.staged and entry.unstaged:
            severity = strict_or_warning(options)
            message = "path has staged and unstaged changes"
        elif entry.staged:
            severity = strict_or_warning(options)
            message = "path has staged changes"
        else:
            severity = strict_or_warning(options)
            message = "path has unstaged changes"

        add_diagnostic(
            diagnostics,
            options,
            severity,
            "KOA-CLEAN-GIT-005",
            f"{message}; status {entry.code!r}",
            entry.path,
            details={"original_path": entry.original_path},
        )

    ignored_process = run_git(
        ["ls-files", "-ci", "--exclude-standard", "-z"],
        repo_root,
    )
    if ignored_process.returncode == 0:
        ignored_tracked = [
            item.decode("utf-8", errors="replace")
            for item in ignored_process.stdout.split(b"\0")
            if item
        ]
        result["ignored_tracked"] = len(ignored_tracked)
        for path in ignored_tracked:
            add_diagnostic(
                diagnostics,
                options,
                "error",
                "KOA-CLEAN-GIT-006",
                "tracked file is also ignored",
                path,
            )

    tracked_process = run_git(["ls-files", "-z"], repo_root)
    if tracked_process.returncode == 0:
        tracked = [
            item.decode("utf-8", errors="replace")
            for item in tracked_process.stdout.split(b"\0")
            if item
        ]
        tracked_forbidden = 0
        for tracked_path in tracked:
            if should_flag_tracked_path(tracked_path, config):
                tracked_forbidden += 1
                add_diagnostic(
                    diagnostics,
                    options,
                    "error",
                    "KOA-CLEAN-GIT-007",
                    "forbidden repository debris is tracked",
                    tracked_path,
                )
        result["tracked_forbidden"] = tracked_forbidden

    submodule_process = run_git(["submodule", "status", "--recursive"], repo_root)
    if submodule_process.returncode == 0:
        submodules = [
            line
            for line in submodule_process.stdout.decode(
                "utf-8", errors="replace"
            ).splitlines()
            if line
        ]
        result["submodules"] = len(submodules)
        for line in submodules:
            marker = line[0]
            if marker in {"-", "+", "U"}:
                add_diagnostic(
                    diagnostics,
                    options,
                    "error",
                    "KOA-CLEAN-GIT-008",
                    "submodule is missing, modified, or conflicted",
                    line[1:].strip(),
                )

    return result


def should_flag_tracked_path(path: str, config: RepositoryConfig) -> bool:
    if is_allowed(path, config):
        return False
    name = PurePosixPath(path).name
    if name in FORBIDDEN_BASENAMES:
        return True
    if any(part in FORBIDDEN_DIRECTORY_NAMES for part in PurePosixPath(path).parts):
        return True
    if path_matches(path, FORBIDDEN_PATH_PATTERNS):
        return True
    if path_matches(path, DOCS_LOCAL_OUTPUT_PATTERNS):
        return True
    return False


def validate_root_relationship(
    options: Options,
    diagnostics: list[Diagnostic],
) -> None:
    if not options.root.exists() or not options.root.is_dir():
        add_diagnostic(
            diagnostics,
            options,
            "error",
            "KOA-CLEAN-ROOT-001",
            f"repository root does not exist: {options.root}",
        )
        return

    if not options.docs_root.exists() or not options.docs_root.is_dir():
        add_diagnostic(
            diagnostics,
            options,
            strict_or_warning(options),
            "KOA-CLEAN-ROOT-002",
            f"documentation root does not exist: {options.docs_root}",
        )
        return

    try:
        options.docs_root.resolve().relative_to(options.root.resolve())
    except ValueError:
        add_diagnostic(
            diagnostics,
            options,
            "error",
            "KOA-CLEAN-ROOT-003",
            "documentation root must be inside the repository root",
            str(options.docs_root),
        )


def run(options: Options) -> Result:
    started_at = now_utc()
    diagnostics: list[Diagnostic] = []
    validate_root_relationship(options, diagnostics)
    config = load_config(options.root, diagnostics, options)

    files: list[Path] = []
    directories: list[Path] = []
    bytes_checked = 0

    if options.root.exists() and options.root.is_dir():
        files, directories = discover_entries(options, config, diagnostics)

        for directory in directories:
            rel = relative(directory, options.root)
            validate_directory(
                directory, rel, config, diagnostics, options
            )

        for path in files:
            rel = relative(path, options.root)
            validate_file_kind(
                path, rel, config, diagnostics, options
            )
            validate_file_name(
                path, rel, config, diagnostics, options
            )
            bytes_checked += validate_file_size(
                path, rel, config, diagnostics, options
            )
            validate_permissions(
                path, rel, diagnostics, options
            )
            scan_secrets(
                path, rel, config, diagnostics, options
            )

        validate_gitignore(
            options.root, config, diagnostics, options
        )

    git_result = validate_git(
        options, config, diagnostics
    )

    categories = Counter(
        item.code.split("-")[2] if len(item.code.split("-")) > 2 else item.code
        for item in diagnostics
    )

    return Result(
        root=str(options.root.resolve()),
        docs_root=str(options.docs_root.resolve()),
        mode="partial" if options.partial else "strict",
        started_at=started_at,
        completed_at=now_utc(),
        files_checked=len(files),
        directories_checked=len(directories),
        bytes_checked=bytes_checked,
        diagnostics=diagnostics,
        git=git_result,
        categories=dict(sorted(categories.items())),
    )


def print_result(result: Result, options: Options) -> None:
    if not options.quiet:
        for diagnostic in sorted(result.diagnostics):
            print(diagnostic.display())
        print(
            "Repository cleanliness "
            + ("passed" if result.passed else "failed")
            + f": {result.files_checked} files, "
            + f"{result.directories_checked} directories, "
            + f"{result.errors} errors, "
            + f"{result.warnings} warnings."
        )

    if options.report_json:
        options.report_json.parent.mkdir(parents=True, exist_ok=True)
        options.report_json.write_text(
            json.dumps(result.to_json(), indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )


def write_clean_fixture(root: Path) -> None:
    docs = root / "docs"
    tools = docs / "tools"
    contracts = docs / "contracts"
    tools.mkdir(parents=True)
    contracts.mkdir(parents=True)

    (root / ".gitignore").write_text(
        "\n".join(
            [
                "__pycache__/",
                "*.py[cod]",
                ".venv/",
                ".pytest_cache/",
                ".mypy_cache/",
                ".ruff_cache/",
                "*.swp",
                "*~",
                ".coverage",
                "htmlcov/",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (docs / "README.md").write_text(
        "# Documentation\n\nClean fixture.\n",
        encoding="utf-8",
    )
    (contracts / "example.json").write_text(
        json.dumps(
            {
                "registry_id": "REG-CLEAN-SELF-001",
                "status": "active",
                "language": "en",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (tools / "example.py").write_text(
        "from __future__ import annotations\n\nprint('clean')\n",
        encoding="utf-8",
    )


def run_self_test(quiet: bool) -> int:
    with tempfile.TemporaryDirectory(
        prefix="koa-clean-repository-"
    ) as temporary:
        root = Path(temporary) / "repo"
        root.mkdir()
        write_clean_fixture(root)

        clean_options = Options(
            root=root,
            docs_root=root / "docs",
            partial=False,
            git_check="never",
            quiet=True,
        )
        clean_result = run(clean_options)

        dirty_path = root / "docs" / "tools" / "local.partial-report.json"
        dirty_path.write_text('{"status":"local"}\n', encoding="utf-8")
        secret_path = root / "docs" / "secret.txt"
        secret_marker = "-----BEGIN " + "PRIVATE KEY-----"
        secret_path.write_text(
            secret_marker + "\nnot-real-but-forbidden\n",
            encoding="utf-8",
        )
        cache_dir = root / "__pycache__"
        cache_dir.mkdir()
        (cache_dir / "example.pyc").write_bytes(b"\x00\x01")

        dirty_options = Options(
            root=root,
            docs_root=root / "docs",
            partial=False,
            git_check="never",
            quiet=True,
        )
        dirty_result = run(dirty_options)

        passed = (
            clean_result.errors == 0
            and dirty_result.errors >= 3
            and any(
                item.code == "KOA-CLEAN-NAME-003"
                for item in dirty_result.diagnostics
            )
            and any(
                item.code == "KOA-CLEAN-SECRET-003"
                for item in dirty_result.diagnostics
            )
        )

        if not quiet:
            if passed:
                print(
                    "Repository-cleanliness self-test passed: "
                    f"clean fixture {clean_result.errors} errors; "
                    f"dirty fixture {dirty_result.errors} errors."
                )
            else:
                print("Repository-cleanliness self-test failed.")
                print("Clean fixture diagnostics:")
                for item in sorted(clean_result.diagnostics):
                    print(item.display())
                print("Dirty fixture diagnostics:")
                for item in sorted(dirty_result.diagnostics):
                    print(item.display())

        return EXIT_OK if passed else EXIT_VALIDATION_ERROR


def build_parser() -> argparse.ArgumentParser:
    default_root, _default_docs_root = infer_roots()
    parser = argparse.ArgumentParser(
        description="Check that the kOA repository is clean and publishable.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """
            Strict mode is the default. Partial mode is suitable during corpus
            construction: unsafe filesystem objects, secret material, tracked
            debris, and forbidden documentation outputs still fail, while
            ordinary Git changes and absent optional repository metadata warn.
            """
        ),
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=default_root,
        help="repository root; defaults to the parent of docs",
    )
    parser.add_argument(
        "--docs-root",
        type=Path,
        default=None,
        help="documentation root; defaults to <root>/docs, or <root> when it is named docs",
    )
    parser.add_argument(
        "--partial",
        action="store_true",
        help="downgrade ordinary working-tree and missing-metadata findings",
    )
    parser.add_argument(
        "--git-check",
        choices=("auto", "always", "never"),
        default="auto",
        help="Git working-tree check mode; default: auto",
    )
    parser.add_argument(
        "--report-json",
        type=Path,
        help="write a machine-readable cleanliness report",
    )
    parser.add_argument(
        "--fail-on-warning",
        action="store_true",
        help="return failure when warnings are present",
    )
    parser.add_argument(
        "--max-diagnostics",
        type=int,
        default=500,
        help="maximum diagnostics retained; default: 500",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="glob relative to the repository root; can be repeated",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="suppress text diagnostics and summary",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="run isolated clean and dirty repository fixtures",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.max_diagnostics < 1:
        parser.error("--max-diagnostics must be at least 1")
    if args.self_test:
        return run_self_test(args.quiet)

    root = args.root.resolve()
    if args.docs_root is not None:
        docs_root = args.docs_root.resolve()
    else:
        docs_root = root if root.name == "docs" else (root / "docs").resolve()

    options = Options(
        root=root,
        docs_root=docs_root,
        partial=args.partial,
        git_check=args.git_check,
        report_json=args.report_json,
        fail_on_warning=args.fail_on_warning,
        max_diagnostics=args.max_diagnostics,
        exclude=tuple(args.exclude),
        quiet=args.quiet,
    )
    result = run(options)
    print_result(result, options)

    failed = result.errors > 0 or (
        options.fail_on_warning and result.warnings > 0
    )
    return EXIT_VALIDATION_ERROR if failed else EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
