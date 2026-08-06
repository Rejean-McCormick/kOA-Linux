from __future__ import annotations

import ast
from pathlib import Path

from koa_semantik_architect_adapter import (
    ArtifactBridge,
    CompilerJobCoordinator,
    LanguageRuntimePackCandidate,
    RuntimePackBridge,
    SemantikArchitectClient,
    create_adapter,
)
from conftest import FakeArtifactAdmission, FakeRuntimeValidation

PACKAGE = Path(__file__).parents[1] / "adapter" / "src" / "koa_semantik_architect_adapter"


def test_no_private_component_or_subsystem_imports():
    forbidden = ("components.", "subsystems.", "koa_kristal_runtime.", "koa_governance_policy_runtime.")
    for path in PACKAGE.glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                names = [node.module or ""]
            else:
                continue
            assert not any(name.startswith(forbidden) for name in names), (path, names)


def test_adapter_contains_no_compiler_or_shell_execution():
    forbidden_calls = {"system", "popen", "run", "call", "check_call", "check_output", "Popen"}
    for path in PACKAGE.glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        assert all(
            not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr in forbidden_calls)
            for node in ast.walk(tree)
        )
        assert "subprocess" not in path.read_text(encoding="utf-8")


def test_bootstrap_uses_only_public_ports(transport, all_capabilities):
    adapter = create_adapter(
        transport=transport,
        artifact_admission_port=FakeArtifactAdmission(),
        runtime_validation_port=FakeRuntimeValidation(),
        capabilities=all_capabilities,
    )
    assert isinstance(adapter.client, SemantikArchitectClient)
    assert isinstance(adapter.compiler_jobs, CompilerJobCoordinator)
    assert isinstance(adapter.artifact_bridge, ArtifactBridge)
    assert isinstance(adapter.runtime_packs, RuntimePackBridge)
    assert adapter.config.documentation_mounted is False


def test_artifact_bridge_moves_references_not_payload_bytes(artifact_candidate):
    port = FakeArtifactAdmission()
    ArtifactBridge(port).admit(
        artifact_candidate, request_id="request:bridge:1", correlation_id="correlation:bridge:1"
    )
    payload = port.calls[0]
    assert payload["content_ref"].startswith("artifact-store:")
    assert "content" not in payload
    assert payload["authority_effect"] == "candidate_only"


def test_runtime_pack_bridge_never_requests_activation(language_pack_manifest):
    port = FakeRuntimeValidation()
    candidate = LanguageRuntimePackCandidate(
        "artifact:pack:boundary",
        "sha256:" + "1" * 64,
        language_pack_manifest,
        "artifact-store:pack:boundary",
        ("evidence:boundary",),
        "provenance:boundary",
        ("release-set:boundary",),
    )
    RuntimePackBridge(port).prepare(
        candidate, request_id="request:boundary", correlation_id="correlation:boundary"
    )
    assert port.calls[0]["activation_requested"] is False
    assert port.calls[0]["authority_effect"] == "candidate_validation_only"
