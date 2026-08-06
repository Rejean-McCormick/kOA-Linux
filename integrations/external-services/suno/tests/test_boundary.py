from __future__ import annotations

import json
from pathlib import Path
import re
import tomllib

import pytest

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_FILES = {
    "README.md",
    "health.toml",
    "integration.toml",
    "policy.toml",
    "tests/test_boundary.py",
    "tests/test_failure.py",
}


def load_toml(name: str) -> dict[str, object]:
    with (ROOT / name).open("rb") as handle:
        return tomllib.load(handle)


def repository_root() -> Path | None:
    for candidate in (ROOT, *ROOT.parents):
        if (candidate / "docs" / "contracts" / "integrations" / "suno.integration.json").is_file():
            return candidate
    return None


def flatten_strings(value: object) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        result: list[str] = []
        for item in value.values():
            result.extend(flatten_strings(item))
        return result
    if isinstance(value, list):
        result = []
        for item in value:
            result.extend(flatten_strings(item))
        return result
    return []


def test_exact_bundle_file_set() -> None:
    actual = {
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    }
    assert actual == EXPECTED_FILES


def test_all_declarations_parse() -> None:
    for name in ("integration.toml", "policy.toml", "health.toml"):
        parsed = load_toml(name)
        assert parsed["schema_version"] == "1.0"
        assert parsed["integration_id"] == "suno"
        assert parsed["status"] == "active"


def test_integration_matches_canonical_contract_when_present() -> None:
    repo = repository_root()
    if repo is None:
        pytest.skip("canonical documentation is not included in the isolated bundle archive")
    canonical = json.loads(
        (repo / "docs" / "contracts" / "integrations" / "suno.integration.json").read_text(
            encoding="utf-8"
        )
    )
    integration = load_toml("integration.toml")
    for key in (
        "integration_id",
        "title",
        "version",
        "status",
        "integration_type",
        "role",
        "authority",
        "availability",
        "undeclared_substitution",
    ):
        assert integration[key] == canonical[key]


def test_closed_capability_and_trigger_boundary() -> None:
    integration = load_toml("integration.toml")
    assert integration["capabilities"] == [
        "user_requested_audio_generation",
        "user_requested_music_generation",
        "candidate_media_artifact_return",
    ]
    assert integration["trigger"] == "explicit_user_action"
    assert integration["activation"] == {
        "profile_permission_required": True,
        "explicit_user_action_required": True,
        "continuous_activation": False,
        "background_sessions": False,
        "operation_scoped": True,
    }


def test_service_is_optional_and_non_authoritative() -> None:
    integration = load_toml("integration.toml")
    assert integration["availability"] == "optional"
    assert integration["authority"] == "non_authoritative"
    assert integration["authority_class"] == "non_authoritative_candidate_source"
    assert integration["enabled_by_default"] is False
    assert integration["direct_authoritative_store_write"] is False
    for key in ("privilege_authority", "policy_authority", "publication_authority", "release_authority"):
        assert integration[key] is False


def test_transfer_is_explicit_minimized_and_store_blind() -> None:
    transfer = load_toml("integration.toml")["data_transfer"]
    assert transfer["disclosure_required"] is True
    assert transfer["explicit_selection_required"] is True
    assert transfer["minimization_required"] is True
    for key in (
        "repository_access",
        "component_store_access",
        "tenant_wide_access",
        "profile_state_access",
        "host_access",
        "secret_access",
    ):
        assert transfer[key] is False


def test_output_remains_candidate_until_local_acceptance() -> None:
    output = load_toml("integration.toml")["output"]
    assert output["result_class"] == "candidate_media_artifact"
    assert output["authoritative"] is False
    assert output["controlled_reimport_required"] is True
    assert output["quarantine_before_acceptance"] is True
    assert output["owning_component_validation_required"] is True
    assert output["user_approval_required"] is True
    assert output["provenance_receipt_required"] is True
    assert output["publication_is_separate"] is True


def test_forbidden_automatic_triggers_are_complete() -> None:
    forbidden = set(load_toml("policy.toml")["invocation"]["forbidden_triggers"])
    required = {
        "ingestion",
        "indexing",
        "classification",
        "tagging",
        "category_generation",
        "routing",
        "synchronization",
        "background_enrichment",
        "publication",
        "backup",
        "restore",
        "uckk_publication",
        "schedule",
        "autonomous_agent",
    }
    assert forbidden == required


def test_publication_is_separate_and_does_not_infer_consent() -> None:
    publication = load_toml("policy.toml")["publication"]
    assert publication["separate_request_required"] is True
    assert publication["gateway_required"] is True
    assert publication["publication_policy_required"] is True
    assert publication["publication_receipt_required"] is True
    assert publication["generation_implies_consent"] is False


def test_no_secret_or_endpoint_value_is_committed() -> None:
    forbidden_key = re.compile(r"(?i)(api[_-]?key|access[_-]?token|client[_-]?secret|password|bearer)")
    forbidden_value = re.compile(r"(?i)(sk-[a-z0-9]{8,}|bearer\s+[a-z0-9._-]+|https?://)")
    for name in ("integration.toml", "policy.toml", "health.toml"):
        data = load_toml(name)
        assert not any(forbidden_key.search(item) for item in flatten_strings(list(data.keys())))
        assert not any(forbidden_value.search(item) for item in flatten_strings(data))


def test_tests_and_declarations_do_not_use_network_clients() -> None:
    forbidden_import = re.compile(
        r"(?m)^\s*(?:from|import)\s+(requests|httpx|aiohttp|urllib3|socket|subprocess)\b"
    )
    for path in (ROOT / "tests").glob("test_*.py"):
        assert forbidden_import.search(path.read_text(encoding="utf-8")) is None, path
    for name in ("README.md", "integration.toml", "policy.toml", "health.toml"):
        text = (ROOT / name).read_text(encoding="utf-8")
        assert "http://" not in text
        assert "https://" not in text
        assert "curl " not in text
        assert "wget " not in text
