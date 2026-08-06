"""Repository secret-scanning tests using synthetic values only."""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]
SCAN_ROOTS = (
    "assembly",
    "ci",
    "components",
    "dev",
    "host",
    "integrations",
    "interfaces",
    "operations",
    "packaging",
    "profiles",
    "release",
    "tools",
)
TEXT_SUFFIXES = {
    ".conf",
    ".env",
    ".ini",
    ".json",
    ".md",
    ".nft",
    ".py",
    ".rs",
    ".service",
    ".sh",
    ".sql",
    ".toml",
    ".yaml",
    ".yml",
}

PRIVATE_KEY_PATTERN = "-----BEGIN " + r"(?:RSA |EC |OPENSSH |DSA )?" + "PRIVATE KEY-----"

PATTERNS = {
    "private key": re.compile(PRIVATE_KEY_PATTERN),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "Slack token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"),
    "generic assigned secret": re.compile(
        r"(?im)^\s*(?:api[_-]?key|access[_-]?token|client[_-]?secret|password|private[_-]?key)\s*[:=]\s*[\"']?([^\s\"'#]{12,})"
    ),
}
PLACEHOLDER_WORDS = {
    "changeme",
    "example",
    "example.invalid",
    "placeholder",
    "redacted",
    "test-only",
    "test_only",
    "not-a-secret",
}


def _find_secrets(text: str) -> list[str]:
    findings: list[str] = []
    lowered = text.lower()
    for label, pattern in PATTERNS.items():
        for match in pattern.finditer(text):
            value = match.group(1) if match.lastindex else match.group(0)
            if any(marker in value.lower() or marker in lowered[max(0, match.start() - 40):match.end() + 40] for marker in PLACEHOLDER_WORDS):
                continue
            findings.append(label)
    return findings


def _tracked_candidate_files() -> list[Path]:
    files: list[Path] = []
    for root_name in SCAN_ROOTS:
        root = ROOT / root_name
        if not root.is_dir():
            continue
        for path in root.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            if any(part in {".git", ".pytest_cache", "__pycache__", "dist", "build"} for part in path.parts):
                continue
            files.append(path)
    return sorted(files)


def test_negative_secret_scanner_detects_synthetic_credentials() -> None:
    synthetic = "\n".join(
        (
            'API_KEY = "' + "synth_" + 'super_secret_value_1234567890"',
            "-----BEGIN " + "PRIVATE KEY-----",
            "not-real-key-material",
            "-----END " + "PRIVATE KEY-----",
            "aws = " + "AKIA" + "ABCDEFGHIJKLMNOP",
        )
    )
    findings = _find_secrets(synthetic)
    assert "generic assigned secret" in findings
    assert "private key" in findings
    assert "AWS access key" in findings


def test_placeholder_values_do_not_require_real_secrets() -> None:
    placeholder = 'password = "not-a-secret"\napi_key = "placeholder"\n'
    assert _find_secrets(placeholder) == []


def test_repository_implementation_roots_contain_no_apparent_secret() -> None:
    findings: list[str] = []
    for path in _tracked_candidate_files():
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for label in _find_secrets(text):
            findings.append(f"{path.relative_to(ROOT)}: {label}")
    assert findings == []
