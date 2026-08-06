from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from koa_assembly.plans import (  # noqa: E402
    DependencyCycleError,
    DependencyGraph,
    DependencyNode,
    UnknownDependencyError,
)


def test_graph_is_acyclic_deterministic_and_layered() -> None:
    graph = DependencyGraph(
        [
            DependencyNode("publication", "publication-gateway", ("governance", "audit")),
            DependencyNode("audit", "audit-broker", ("identity",)),
            DependencyNode("identity", "identity-and-trust"),
            DependencyNode("governance", "governance-policy-runtime", ("identity",)),
        ]
    )

    assert graph.order == ("identity", "audit", "governance", "publication")
    assert graph.layers == (
        ("identity",),
        ("audit", "governance"),
        ("publication",),
    )
    assert graph.transitive_dependencies("publication") == (
        "identity",
        "audit",
        "governance",
    )
    assert graph.dependents("identity") == ("audit", "governance")
    assert json.dumps(graph.to_dict(), sort_keys=True) == json.dumps(graph.to_dict(), sort_keys=True)


def test_graph_rejects_unknown_dependency() -> None:
    with pytest.raises(UnknownDependencyError, match="unknown dependencies"):
        DependencyGraph([DependencyNode("service", "owner", ("missing",))])


def test_graph_reports_cycle_path() -> None:
    with pytest.raises(DependencyCycleError) as error:
        DependencyGraph(
            [
                DependencyNode("a", "owner-a", ("b",)),
                DependencyNode("b", "owner-b", ("c",)),
                DependencyNode("c", "owner-c", ("a",)),
            ]
        )
    cycle = error.value.cycle
    assert cycle[0] == cycle[-1]
    assert set(cycle[:-1]) == {"a", "b", "c"}
