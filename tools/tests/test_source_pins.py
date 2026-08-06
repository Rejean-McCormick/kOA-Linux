from __future__ import annotations

import json
from pathlib import Path

import pytest

from koa_tools.checks.runtime_paths import (
    RuntimePathError,
    check as check_runtime_paths,
    normalize_runtime_path,
    validate_runtime_paths,
)
from koa_tools.checks.source_pins import (
    SourcePinError,
    check as check_source_pins,
    check_source_pins_file,
    validate_source_pins,
)
from koa_tools.config import ConfigurationError, load_json_object, normalize_repository_path
from koa_tools.repository import Repository, RepositoryError

SHA256 = "a" * 64
COMMIT = "b" * 40


def pin(**overrides: object) -> dict[str, object]:
    value: dict[str, object] = {
        "source_id": "ariane",
        "source_type": "git",
        "location": "https://example.invalid/ariane.git",
        "revision": COMMIT,
        "owner": "integration:ariane",
        "lock_file": "integrations/ariane/source.lock.json",
    }
    value.update(overrides)
    return value


def document(*pins: dict[str, object]) -> dict[str, object]:
    return {"schema_version": 1, "sources": list(pins)}


def test_valid_git_commit_pin() -> None:
    pins = validate_source_pins(document(pin()))
    assert len(pins) == 1
    assert pins[0].source_id == "ariane"
    assert pins[0].digest is None


def test_version_tag_requires_digest() -> None:
    with pytest.raises(SourcePinError, match="requires an exact sha256 digest"):
        validate_source_pins(document(pin(revision="v2.3.1")))


def test_version_tag_with_digest_is_exact() -> None:
    pins = validate_source_pins(
        document(pin(revision="v2.3.1", digest={"algorithm": "sha256", "value": SHA256}))
    )
    assert pins[0].revision == "v2.3.1"


@pytest.mark.parametrize("revision", ["main", "latest", "refs/heads/release", "v2.*", "snapshot"])
def test_floating_revision_fails_closed(revision: str) -> None:
    with pytest.raises(SourcePinError, match="mutable|floating"):
        validate_source_pins(
            document(pin(revision=revision, digest={"algorithm": "sha256", "value": SHA256}))
        )


def test_archive_requires_digest() -> None:
    with pytest.raises(SourcePinError, match="digest: required"):
        validate_source_pins(
            document(
                pin(
                    source_type="archive",
                    location="https://example.invalid/ariane.tar.zst",
                    revision="2.3.1",
                )
            )
        )


def test_digest_must_be_lowercase_sha256() -> None:
    with pytest.raises(SourcePinError, match="64 lowercase hexadecimal"):
        validate_source_pins(
            document(pin(digest={"algorithm": "sha256", "value": "A" * 64}))
        )


def test_duplicate_source_identity_is_rejected() -> None:
    with pytest.raises(SourcePinError, match="duplicate 'ariane'"):
        validate_source_pins(document(pin(), pin(lock_file="integrations/other/source.lock.json")))


def test_lock_path_traversal_is_rejected() -> None:
    with pytest.raises(ConfigurationError, match=r"'\.\.'"):
        validate_source_pins(document(pin(lock_file="integrations/ariane/../source.lock.json")))


def test_embedded_credentials_are_rejected() -> None:
    with pytest.raises(SourcePinError, match="embedded credentials"):
        validate_source_pins(
            document(pin(location="https://user:secret@example.invalid/ariane.git"))
        )


def test_unknown_fields_are_rejected() -> None:
    with pytest.raises(ConfigurationError, match="unknown keys"):
        validate_source_pins(document(pin(branch="main")))


@pytest.mark.parametrize("version", [True, 1.0, 2, "1"])
def test_schema_version_must_be_exact_integer(version: object) -> None:
    with pytest.raises(SourcePinError, match="schema_version"):
        validate_source_pins({"schema_version": version, "sources": [pin()]})


def test_file_check_returns_stable_issue(tmp_path: Path) -> None:
    path = tmp_path / "source-pins.json"
    path.write_text(json.dumps(document(pin(revision="main"))), encoding="utf-8")
    result = check_source_pins_file(path)
    assert not result.ok
    assert result.issues[0].code == "source_pins_invalid"


def test_json_loader_rejects_duplicate_keys(tmp_path: Path) -> None:
    path = tmp_path / "duplicate.json"
    path.write_text('{"schema_version": 1, "schema_version": 1}', encoding="utf-8")
    with pytest.raises(ConfigurationError, match="duplicate JSON key"):
        load_json_object(path)


@pytest.mark.parametrize(
    "value",
    ["../secret", "components/../secret", "/absolute", "a//b", "a/./b", "a\\b", "a/"],
)
def test_repository_path_normalization_rejects_ambiguous_paths(value: str) -> None:
    with pytest.raises(ConfigurationError):
        normalize_repository_path(value)


def test_repository_resolution_rejects_symlink_escape(tmp_path: Path) -> None:
    repository_root = tmp_path / "repo"
    repository_root.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    (repository_root / "escape").symlink_to(outside, target_is_directory=True)
    repository = Repository(repository_root)
    with pytest.raises(RepositoryError, match="escapes"):
        repository.resolve("escape/config.json")


def test_repository_resolution_rejects_broken_symlink_escape(tmp_path: Path) -> None:
    repository_root = tmp_path / "repo"
    repository_root.mkdir()
    (repository_root / "escape").symlink_to(tmp_path / "missing-outside", target_is_directory=True)
    repository = Repository(repository_root)
    with pytest.raises(RepositoryError, match="escapes"):
        repository.resolve("escape/config.json")


def test_missing_control_files_return_closed_results(tmp_path: Path) -> None:
    repository = Repository(tmp_path)
    source_result = check_source_pins(repository)
    runtime_result = check_runtime_paths(repository)
    assert not source_result.ok
    assert source_result.issues[0].code == "source_pins_unavailable"
    assert not runtime_result.ok
    assert runtime_result.issues[0].code == "runtime_paths_unavailable"


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        ("/usr/libexec/koa/koa-node-agent", "/usr/libexec/koa/koa-node-agent"),
        ("/etc/koa/node/config.toml", "/etc/koa/node/config.toml"),
        ("/run/koa/sockets/audit-broker.sock", "/run/koa/sockets/audit-broker.sock"),
        ("/var/lib/koa/receipts/item.json", "/var/lib/koa/receipts/item.json"),
        ("/var/cache/koa-build/workers/worker-1", "/var/cache/koa-build/workers/worker-1"),
    ],
)
def test_runtime_path_normalization(path: str, expected: str) -> None:
    assert normalize_runtime_path(path) == expected


@pytest.mark.parametrize(
    "path",
    ["relative", "/tmp/koa", "/run/koa/../etc", "/run//koa", "/run/koa/"],
)
def test_runtime_path_rejects_unknown_or_noncanonical_paths(path: str) -> None:
    with pytest.raises(RuntimePathError):
        normalize_runtime_path(path)


def test_runtime_mapping_class_must_match_frozen_root() -> None:
    with pytest.raises(RuntimePathError, match="does not match"):
        validate_runtime_paths(
            {
                "schema_version": 1,
                "mappings": [
                    {
                        "source": "host/systemd/units/koa-node-agent.service",
                        "destination": "/usr/lib/systemd/system/koa-node-agent.service",
                        "path_class": "persistent_state",
                        "owner": "host",
                    }
                ],
            }
        )
