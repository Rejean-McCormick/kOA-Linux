"""Deterministic, closed dependency graphs used by assembly plans."""

from __future__ import annotations

from dataclasses import dataclass, field
from heapq import heappop, heappush
from types import MappingProxyType
from typing import Iterable, Mapping


class PlanValidationError(ValueError):
    """Raised when an assembly plan is not closed, deterministic, or safe."""


class UnknownDependencyError(PlanValidationError):
    """Raised when a dependency points outside the closed graph."""


class DependencyCycleError(PlanValidationError):
    """Raised when a dependency cycle prevents deterministic ordering."""

    def __init__(self, cycle: Iterable[str]) -> None:
        self.cycle = tuple(cycle)
        super().__init__("dependency cycle: " + " -> ".join(self.cycle))


@dataclass(frozen=True, slots=True)
class DependencyNode:
    """One owner-preserving node in a dependency graph."""

    node_id: str
    owner_id: str
    dependencies: tuple[str, ...] = field(default_factory=tuple)
    kind: str = "service"

    def __post_init__(self) -> None:
        node_id = _identifier(self.node_id, "node_id")
        owner_id = _identifier(self.owner_id, "owner_id")
        kind = _identifier(self.kind, "kind")
        dependencies = tuple(sorted({_identifier(item, "dependency") for item in self.dependencies}))
        if node_id in dependencies:
            raise DependencyCycleError((node_id, node_id))
        object.__setattr__(self, "node_id", node_id)
        object.__setattr__(self, "owner_id", owner_id)
        object.__setattr__(self, "kind", kind)
        object.__setattr__(self, "dependencies", dependencies)


class DependencyGraph:
    """An immutable, acyclic graph whose complete node set is known up front."""

    def __init__(self, nodes: Iterable[DependencyNode]) -> None:
        by_id: dict[str, DependencyNode] = {}
        for node in nodes:
            if node.node_id in by_id:
                raise PlanValidationError(f"duplicate dependency node: {node.node_id}")
            by_id[node.node_id] = node
        if not by_id:
            raise PlanValidationError("dependency graph must contain at least one node")

        known = frozenset(by_id)
        for node in by_id.values():
            unknown = sorted(set(node.dependencies) - known)
            if unknown:
                raise UnknownDependencyError(
                    f"{node.node_id} references unknown dependencies: {', '.join(unknown)}"
                )

        self._nodes = MappingProxyType(dict(sorted(by_id.items())))
        self._order = self._topological_order()
        self._layers = self._topological_layers()

    @classmethod
    def from_mapping(
        cls,
        dependencies: Mapping[str, Iterable[str]],
        *,
        owners: Mapping[str, str] | None = None,
        kinds: Mapping[str, str] | None = None,
    ) -> "DependencyGraph":
        owners = owners or {}
        kinds = kinds or {}
        nodes = (
            DependencyNode(
                node_id=node_id,
                owner_id=owners.get(node_id, node_id),
                dependencies=tuple(required),
                kind=kinds.get(node_id, "service"),
            )
            for node_id, required in dependencies.items()
        )
        return cls(nodes)

    @property
    def nodes(self) -> Mapping[str, DependencyNode]:
        return self._nodes

    @property
    def order(self) -> tuple[str, ...]:
        """Dependencies-first deterministic order."""

        return self._order

    @property
    def layers(self) -> tuple[tuple[str, ...], ...]:
        """Parallelizable dependency layers, dependencies before consumers."""

        return self._layers

    def transitive_dependencies(self, node_id: str) -> tuple[str, ...]:
        node_id = _identifier(node_id, "node_id")
        if node_id not in self._nodes:
            raise UnknownDependencyError(f"unknown dependency node: {node_id}")
        found: set[str] = set()
        pending = list(self._nodes[node_id].dependencies)
        while pending:
            current = pending.pop()
            if current in found:
                continue
            found.add(current)
            pending.extend(self._nodes[current].dependencies)
        return tuple(item for item in self._order if item in found)

    def dependents(self, node_id: str) -> tuple[str, ...]:
        node_id = _identifier(node_id, "node_id")
        if node_id not in self._nodes:
            raise UnknownDependencyError(f"unknown dependency node: {node_id}")
        direct = [
            candidate.node_id
            for candidate in self._nodes.values()
            if node_id in candidate.dependencies
        ]
        return tuple(sorted(direct))

    def to_dict(self) -> dict[str, object]:
        return {
            "nodes": [
                {
                    "node_id": node.node_id,
                    "owner_id": node.owner_id,
                    "kind": node.kind,
                    "dependencies": list(node.dependencies),
                }
                for node in self._nodes.values()
            ],
            "order": list(self._order),
            "layers": [list(layer) for layer in self._layers],
        }

    def _topological_order(self) -> tuple[str, ...]:
        indegree = {node_id: len(node.dependencies) for node_id, node in self._nodes.items()}
        dependents: dict[str, list[str]] = {node_id: [] for node_id in self._nodes}
        for node in self._nodes.values():
            for dependency in node.dependencies:
                dependents[dependency].append(node.node_id)
        ready: list[str] = []
        for node_id, degree in indegree.items():
            if degree == 0:
                heappush(ready, node_id)
        ordered: list[str] = []
        while ready:
            node_id = heappop(ready)
            ordered.append(node_id)
            for dependent in sorted(dependents[node_id]):
                indegree[dependent] -= 1
                if indegree[dependent] == 0:
                    heappush(ready, dependent)
        if len(ordered) != len(self._nodes):
            raise DependencyCycleError(self._find_cycle())
        return tuple(ordered)

    def _topological_layers(self) -> tuple[tuple[str, ...], ...]:
        remaining = set(self._nodes)
        completed: set[str] = set()
        layers: list[tuple[str, ...]] = []
        while remaining:
            layer = tuple(
                sorted(
                    node_id
                    for node_id in remaining
                    if set(self._nodes[node_id].dependencies) <= completed
                )
            )
            if not layer:
                raise DependencyCycleError(self._find_cycle())
            layers.append(layer)
            completed.update(layer)
            remaining.difference_update(layer)
        return tuple(layers)

    def _find_cycle(self) -> tuple[str, ...]:
        state: dict[str, int] = {node_id: 0 for node_id in self._nodes}
        stack: list[str] = []

        def visit(node_id: str) -> tuple[str, ...] | None:
            state[node_id] = 1
            stack.append(node_id)
            for dependency in self._nodes[node_id].dependencies:
                if state[dependency] == 0:
                    cycle = visit(dependency)
                    if cycle:
                        return cycle
                elif state[dependency] == 1:
                    start = stack.index(dependency)
                    return tuple(stack[start:] + [dependency])
            stack.pop()
            state[node_id] = 2
            return None

        for node_id in sorted(self._nodes):
            if state[node_id] == 0:
                cycle = visit(node_id)
                if cycle:
                    return cycle
        return tuple()


def _identifier(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise PlanValidationError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise PlanValidationError(f"{field_name} must not be empty")
    if normalized != value:
        raise PlanValidationError(f"{field_name} must not contain surrounding whitespace")
    if any(character.isspace() for character in normalized):
        raise PlanValidationError(f"{field_name} must not contain whitespace: {value!r}")
    return normalized
