#!/usr/bin/env python3
"""
Compute direct and transitive documentation impact for kOA.

The tool builds a typed reverse-dependency graph from active Markdown metadata,
JSON registries and contracts, accepted ADR ownership, generated-source
relationships, requirement projections, locks, exceptions, and ordinary
repo-relative references.

It can:

* analyze explicit paths, JSON Pointers, object IDs, and decision IDs;
* discover changed documentation files from Git when available;
* emit a machine-readable impact report;
* validate the graph in read-only ``--check-clean`` mode;
* accept reviewed impact dispositions from a separate JSON file.

The graph and report contain no generic source, metadata, or generated-prose
hashes. Intrinsic artifact integrity remains owned by the relevant artifact
contracts.
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import enum
import json
import os
import re
import subprocess
import sys
import tempfile
from collections import defaultdict, deque
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Iterator, Mapping, Sequence


DOC_META_PATTERN = re.compile(
    r"<!-- KOA:DOC-META:BEGIN GENERATED\n(.*?)\nKOA:DOC-META:END -->",
    re.DOTALL,
)
REQUIREMENT_LINE_PATTERN = re.compile(
    r"^- \*\*(REQ-[A-Z0-9-]+) — "
    r"(SHALL NOT|SHALL|SHOULD NOT|SHOULD|MAY):\*\* (.+)$",
    re.MULTILINE,
)
ID_PATTERN = re.compile(
    r"^(?:"
    r"ADR|AICTX|ART-CLASS|CHG|COMP|DEC|DOC|EVID|EXC|IMPACT|LOCK|"
    r"MIG|PROFILE|RECIPE|REQ|SRC|TERM|TEST|TOOL"
    r")(?:-[A-Z0-9]+)+$"
)
PATH_SUFFIXES = (
    ".md",
    ".json",
    ".jsonl",
    ".py",
    ".yaml",
    ".yml",
    ".toml",
    ".txt",
)
IDENTITY_KEYS = (
    "decision_id",
    "requirement_id",
    "lock_id",
    "exception_id",
    "adr_id",
    "doc_id",
    "component_id",
    "profile_id",
    "artifact_class_id",
    "term_id",
    "test_id",
    "evidence_id",
    "context_id",
    "registry_id",
    "schema_id",
    "recipe_id",
    "toolchain_id",
    "migration_id",
    "source_id",
    "change_id",
    "impact_id",
    "id",
)
REFERENCE_KEYS = {
    "canonical_ref",
    "canonical_refs",
    "source_ref",
    "source_refs",
    "references",
    "reference",
    "decision_ids",
    "requirement_ids",
    "lock_ids",
    "exception_ids",
    "depends_on",
    "dependency_refs",
    "dependencies",
    "included_in",
    "includes",
    "adopts",
    "inherits",
    "maps_from",
    "generated_from",
    "source_documents",
    "read_order",
    "supersedes",
    "replaced_by",
    "superseded_by",
    "validated_by",
    "evidenced_by",
    "test_refs",
    "evidence_refs",
    "profile_refs",
    "component_refs",
    "artifact_refs",
    "release_channel_refs",
    "$ref",
    "schema_ref",
}
ALLOWED_DISPOSITIONS = {
    "updated",
    "reviewed_no_change",
    "regenerated",
    "deprecated",
    "superseded",
    "exception_applied",
    "blocked",
}
SEMANTIC_CLASSES = {"patch", "minor", "major", "unclassified"}


class ImpactError(RuntimeError):
    """Raised for a user-actionable impact-analysis error."""


class Severity(str, enum.Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclasses.dataclass(frozen=True)
class Diagnostic:
    code: str
    severity: Severity
    message: str
    path: str | None = None
    pointer: str | None = None
    object_id: str | None = None

    def as_dict(self) -> dict[str, Any]:
        result = dataclasses.asdict(self)
        result["severity"] = self.severity.value
        return {key: value for key, value in result.items() if value is not None}


@dataclasses.dataclass
class Node:
    key: str
    object_id: str
    object_type: str
    path: str | None = None
    pointer: str | None = None
    document_class: str | None = None
    layer: str | None = None
    status: str | None = None
    generated: bool = False
    defined: bool = False
    details: dict[str, Any] = dataclasses.field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        result = {
            "object_id": self.object_id,
            "object_type": self.object_type,
            "path": self.path,
            "pointer": self.pointer,
            "document_class": self.document_class,
            "layer": self.layer,
            "status": self.status,
            "generated": self.generated,
            "defined": self.defined,
        }
        if self.details:
            result["details"] = self.details
        return {key: value for key, value in result.items() if value is not None}


@dataclasses.dataclass(frozen=True)
class Edge:
    source: str
    target: str
    relationship: str
    evidence_path: str | None = None
    evidence_pointer: str | None = None

    def as_dict(self, graph: "ImpactGraph") -> dict[str, Any]:
        result = {
            "source": graph.nodes[self.source].object_id,
            "target": graph.nodes[self.target].object_id,
            "relationship": self.relationship,
            "evidence_path": self.evidence_path,
            "evidence_pointer": self.evidence_pointer,
        }
        return {key: value for key, value in result.items() if value is not None}


@dataclasses.dataclass
class TraversalRecord:
    node_key: str
    distance: int
    predecessor: str | None
    edge: Edge | None
    seed: str


@dataclasses.dataclass
class Disposition:
    disposition: str
    reviewer: str | None = None
    reviewed_on: str | None = None
    rationale: str | None = None
    exception_id: str | None = None
    blocker: str | None = None

    def validate(self, target: str) -> None:
        if self.disposition not in ALLOWED_DISPOSITIONS:
            raise ImpactError(
                f"Unsupported disposition {self.disposition!r} for {target}. "
                f"Allowed: {', '.join(sorted(ALLOWED_DISPOSITIONS))}."
            )
        if self.disposition == "reviewed_no_change":
            missing = [
                name
                for name, value in (
                    ("reviewer", self.reviewer),
                    ("reviewed_on", self.reviewed_on),
                    ("rationale", self.rationale),
                )
                if not value
            ]
            if missing:
                raise ImpactError(
                    f"Disposition reviewed_no_change for {target} is missing: "
                    f"{', '.join(missing)}."
                )
        if self.disposition == "exception_applied" and not self.exception_id:
            raise ImpactError(
                f"Disposition exception_applied for {target} requires exception_id."
            )
        if self.disposition == "blocked" and not self.blocker:
            self.blocker = "review_or_authority_required"

    def as_dict(self) -> dict[str, Any]:
        result = dataclasses.asdict(self)
        return {key: value for key, value in result.items() if value is not None}


class ImpactGraph:
    """Typed directed graph whose edges point from a changed fact to dependents."""

    def __init__(self, repo_root: Path, docs_root: Path) -> None:
        self.repo_root = repo_root.resolve()
        self.docs_root = docs_root.resolve()
        self.nodes: dict[str, Node] = {}
        self.edges: dict[str, list[Edge]] = defaultdict(list)
        self.aliases: dict[str, set[str]] = defaultdict(set)
        self.diagnostics: list[Diagnostic] = []
        self._edge_keys: set[tuple[str, str, str, str | None, str | None]] = set()

    def add_node(self, node: Node, aliases: Iterable[str] = ()) -> str:
        existing = self.nodes.get(node.key)
        if existing is None:
            self.nodes[node.key] = node
        else:
            self._merge_node(existing, node)
        self.add_alias(node.object_id, node.key)
        if node.path:
            self.add_alias(node.path, node.key)
            if node.path.startswith("docs/"):
                self.add_alias(node.path.removeprefix("docs/"), node.key)
            if node.pointer:
                self.add_alias(f"{node.path}#{node.pointer}", node.key)
                if node.path.startswith("docs/"):
                    self.add_alias(
                        f"{node.path.removeprefix('docs/')}#{node.pointer}",
                        node.key,
                    )
        for alias in aliases:
            self.add_alias(alias, node.key)
        return node.key

    def _merge_node(self, existing: Node, incoming: Node) -> None:
        for field_name in (
            "path",
            "pointer",
            "document_class",
            "layer",
            "status",
        ):
            current = getattr(existing, field_name)
            new_value = getattr(incoming, field_name)
            if current is None and new_value is not None:
                setattr(existing, field_name, new_value)
        existing.generated = existing.generated or incoming.generated
        existing.defined = existing.defined or incoming.defined
        if existing.object_type in {"identifier", "reference"} and incoming.object_type:
            existing.object_type = incoming.object_type
        existing.details.update(incoming.details)

    def add_alias(self, alias: str, node_key: str) -> None:
        normalized = alias.strip()
        if normalized:
            self.aliases[normalized].add(node_key)

    def ensure_identifier(
        self,
        identifier: str,
        object_type: str | None = None,
        *,
        defined: bool = False,
        details: Mapping[str, Any] | None = None,
    ) -> str:
        key = f"id:{identifier}"
        inferred_type = object_type or infer_object_type_from_id(identifier)
        return self.add_node(
            Node(
                key=key,
                object_id=identifier,
                object_type=inferred_type,
                defined=defined,
                details=dict(details or {}),
            )
        )

    def ensure_reference(
        self,
        reference: str,
        current_path: str | None = None,
    ) -> str:
        normalized = normalize_reference(reference, current_path, self.repo_root)
        resolved = self.resolve_alias(normalized)
        if len(resolved) == 1:
            return resolved[0]

        path_part, pointer = split_reference(normalized)
        key = f"ref:{normalized}"
        object_id = normalized
        object_type = "json_pointer" if pointer else "reference"
        return self.add_node(
            Node(
                key=key,
                object_id=object_id,
                object_type=object_type,
                path=path_part if looks_like_path(path_part) else None,
                pointer=pointer,
                defined=False,
            ),
            aliases=(reference, normalized),
        )

    def add_edge(
        self,
        source: str,
        target: str,
        relationship: str,
        *,
        evidence_path: str | None = None,
        evidence_pointer: str | None = None,
    ) -> None:
        if source == target:
            return
        edge_key = (
            source,
            target,
            relationship,
            evidence_path,
            evidence_pointer,
        )
        if edge_key in self._edge_keys:
            return
        self._edge_keys.add(edge_key)
        self.edges[source].append(
            Edge(
                source=source,
                target=target,
                relationship=relationship,
                evidence_path=evidence_path,
                evidence_pointer=evidence_pointer,
            )
        )

    def resolve_alias(self, alias: str) -> list[str]:
        direct = sorted(self.aliases.get(alias, set()))
        if direct:
            return direct

        normalized = alias.strip().replace("\\", "/")
        direct = sorted(self.aliases.get(normalized, set()))
        if direct:
            return direct

        if normalized.startswith("./"):
            direct = sorted(self.aliases.get(normalized[2:], set()))
            if direct:
                return direct

        if not normalized.startswith("docs/") and looks_like_path(
            split_reference(normalized)[0]
        ):
            direct = sorted(self.aliases.get(f"docs/{normalized}", set()))
            if direct:
                return direct

        return []

    def traverse(self, seeds: Sequence[str], max_depth: int | None) -> dict[str, TraversalRecord]:
        records: dict[str, TraversalRecord] = {}
        queue: deque[str] = deque()

        for seed in seeds:
            records[seed] = TraversalRecord(
                node_key=seed,
                distance=0,
                predecessor=None,
                edge=None,
                seed=seed,
            )
            queue.append(seed)

        while queue:
            source = queue.popleft()
            record = records[source]
            if max_depth is not None and record.distance >= max_depth:
                continue

            for edge in sorted(
                self.edges.get(source, []),
                key=lambda item: (
                    item.relationship,
                    self.nodes[item.target].object_id,
                    item.target,
                ),
            ):
                if edge.target in records:
                    continue
                records[edge.target] = TraversalRecord(
                    node_key=edge.target,
                    distance=record.distance + 1,
                    predecessor=source,
                    edge=edge,
                    seed=record.seed,
                )
                queue.append(edge.target)

        return records

    def unresolved_nodes(self) -> list[Node]:
        return sorted(
            (
                node
                for node in self.nodes.values()
                if not node.defined and node.object_type in {
                    "decision",
                    "requirement",
                    "lock",
                    "exception",
                    "document",
                    "adr",
                    "profile",
                    "component",
                    "test",
                    "evidence",
                    "json_pointer",
                    "reference",
                }
            ),
            key=lambda node: (node.object_type, node.object_id),
        )

    def collapse_resolved_references(self) -> None:
        """Merge path and pointer placeholders after all source objects are indexed."""
        replacements: dict[str, str] = {}

        for node_key, node in list(self.nodes.items()):
            if node.defined or node.object_type not in {"reference", "json_pointer"}:
                continue

            candidate_aliases = [node.object_id]
            if node.path:
                candidate_aliases.append(node.path)
                if node.pointer:
                    candidate_aliases.append(f"{node.path}#{node.pointer}")

            candidates: set[str] = set()
            for alias in candidate_aliases:
                candidates.update(self.aliases.get(alias, set()))
            candidates.discard(node_key)
            candidates = {
                candidate
                for candidate in candidates
                if candidate in self.nodes and self.nodes[candidate].defined
            }

            if len(candidates) == 1:
                replacements[node_key] = next(iter(candidates))

        if not replacements:
            return

        rebuilt: dict[str, list[Edge]] = defaultdict(list)
        rebuilt_keys: set[tuple[str, str, str, str | None, str | None]] = set()

        for edges in self.edges.values():
            for edge in edges:
                source = replacements.get(edge.source, edge.source)
                target = replacements.get(edge.target, edge.target)
                if source == target:
                    continue
                edge_key = (
                    source,
                    target,
                    edge.relationship,
                    edge.evidence_path,
                    edge.evidence_pointer,
                )
                if edge_key in rebuilt_keys:
                    continue
                rebuilt_keys.add(edge_key)
                rebuilt[source].append(
                    Edge(
                        source=source,
                        target=target,
                        relationship=edge.relationship,
                        evidence_path=edge.evidence_path,
                        evidence_pointer=edge.evidence_pointer,
                    )
                )

        for alias, keys in self.aliases.items():
            updated = {replacements.get(key, key) for key in keys}
            keys.clear()
            keys.update(updated)

        for old_key in replacements:
            self.nodes.pop(old_key, None)

        self.edges = rebuilt
        self._edge_keys = rebuilt_keys

    def graph_summary(self) -> dict[str, Any]:
        return {
            "node_count": len(self.nodes),
            "edge_count": sum(len(edges) for edges in self.edges.values()),
            "alias_count": len(self.aliases),
            "diagnostic_count": len(self.diagnostics),
            "unresolved_node_count": len(self.unresolved_nodes()),
        }


def infer_object_type_from_id(identifier: str) -> str:
    prefix_map = {
        "ADR-": "adr",
        "AICTX-": "ai_context",
        "ART-CLASS-": "artifact_class",
        "CHG-": "change",
        "COMP-": "component",
        "DEC-": "decision",
        "DOC-": "document",
        "EVID-": "evidence",
        "EXC-": "exception",
        "IMPACT-": "impact_report",
        "LOCK-": "lock",
        "MIG-": "migration",
        "PROFILE-": "profile",
        "RECIPE-": "recipe",
        "REQ-": "requirement",
        "SRC-": "source",
        "TERM-": "term",
        "TEST-": "test",
        "TOOL-": "tool",
    }
    for prefix, object_type in prefix_map.items():
        if identifier.startswith(prefix):
            return object_type
    return "identifier"


def looks_like_id(value: str) -> bool:
    return bool(ID_PATTERN.fullmatch(value.strip()))


def looks_like_path(value: str) -> bool:
    candidate = value.strip().replace("\\", "/")
    path_part, pointer = split_reference(candidate)

    if pointer is not None and path_part == "":
        return True
    if not path_part or any(character.isspace() for character in path_part):
        return False
    if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*://", path_part):
        return False
    if path_part.startswith(("urn:", "data:", "^", "$")):
        return False

    first_segment = path_part.lstrip("./").split("/", 1)[0]
    recognized_root = (
        first_segment in {
            "docs",
            "doc",
            "contracts",
            "schemas",
            "generated",
            "tools",
            "archive",
        }
        or bool(re.fullmatch(r"[0-9]{2}-[a-z0-9-]+", first_segment))
    )
    return (
        path_part.endswith(PATH_SUFFIXES)
        or path_part.startswith(("./", "../"))
        or recognized_root
    )


def split_reference(reference: str) -> tuple[str, str | None]:
    if "#" not in reference:
        return reference, None
    path_part, fragment = reference.split("#", 1)
    pointer = fragment if fragment.startswith("/") else f"/{fragment}" if fragment else "/"
    return path_part, pointer


def normalize_reference(
    reference: str,
    current_path: str | None,
    repo_root: Path,
) -> str:
    raw = reference.strip().replace("\\", "/")
    path_part, pointer = split_reference(raw)

    if looks_like_id(path_part) and pointer is None:
        return path_part

    if not path_part:
        normalized_path = current_path or ""
    elif path_part.startswith("/"):
        try:
            normalized_path = Path(path_part).resolve().relative_to(repo_root).as_posix()
        except ValueError:
            normalized_path = path_part
    else:
        if path_part.startswith("docs/"):
            base = PurePosixPath(".")
        elif (
            path_part.startswith("contracts/")
            or path_part.startswith("schemas/")
            or path_part.startswith("generated/")
            or path_part.startswith("tools/")
            or path_part[0:3].isdigit()
        ):
            base = PurePosixPath("docs")
        elif current_path:
            base = PurePosixPath(current_path).parent
        else:
            base = PurePosixPath("docs")

        combined = base / PurePosixPath(path_part)
        parts: list[str] = []
        for part in combined.parts:
            if part in ("", "."):
                continue
            if part == "..":
                if parts:
                    parts.pop()
                continue
            parts.append(part)
        normalized_path = PurePosixPath(*parts).as_posix()

        if not normalized_path.startswith("docs/") and (
            normalized_path.startswith("contracts/")
            or normalized_path.startswith("schemas/")
            or normalized_path.startswith("generated/")
            or normalized_path.startswith("tools/")
            or normalized_path[0:3].isdigit()
        ):
            normalized_path = f"docs/{normalized_path}"

    if pointer is None:
        return normalized_path
    return f"{normalized_path}#{pointer}"


def json_pointer_escape(token: str) -> str:
    return token.replace("~", "~0").replace("/", "~1")


def iter_scalar_strings(value: Any) -> Iterator[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from iter_scalar_strings(item)


def identity_from_object(value: Mapping[str, Any]) -> tuple[str | None, str | None]:
    for key in IDENTITY_KEYS:
        candidate = value.get(key)
        if isinstance(candidate, str) and looks_like_id(candidate):
            return candidate, key
    return None, None


def relationship_for_key(key: str, owner_to_target: bool = False) -> tuple[str, bool]:
    normalized = key.lower()
    if normalized in {"validated_by", "test_refs"}:
        return "validated_by", True
    if normalized in {"evidenced_by", "evidence_refs"}:
        return "evidenced_by", True
    if normalized in {"replaced_by", "superseded_by"}:
        return normalized, True
    if normalized == "supersedes":
        return "superseded_by", False
    if normalized in {"generated_from", "source_documents", "read_order"}:
        return "generated_from", False
    if normalized in {"depends_on", "dependencies", "dependency_refs"}:
        return "depended_on_by", False
    if normalized in {"adopts", "inherits", "included_in", "includes"}:
        return normalized, False
    if normalized == "maps_from":
        return "mapped_to", False
    return "referenced_by", owner_to_target


class CorpusIndexer:
    def __init__(self, graph: ImpactGraph) -> None:
        self.graph = graph
        self.files: list[Path] = []

    def build(self) -> None:
        self._discover_files()
        self._register_file_nodes()
        for path in self.files:
            suffix = path.suffix.lower()
            if suffix == ".md":
                self._index_markdown(path)
            elif suffix in {".json", ".jsonl"}:
                self._index_json(path)
        self.graph.collapse_resolved_references()

    def _discover_files(self) -> None:
        ignored_parts = {".git", "__pycache__", ".venv", "node_modules"}
        self.files = sorted(
            path
            for path in self.graph.docs_root.rglob("*")
            if path.is_file() and not ignored_parts.intersection(path.parts)
        )

    def _register_file_nodes(self) -> None:
        for path in self.files:
            rel = path.relative_to(self.graph.repo_root).as_posix()
            docs_rel = path.relative_to(self.graph.docs_root).as_posix()
            generated = docs_rel.startswith("generated/")
            object_type = "generated_file" if generated else "file"
            key = f"file:{rel}"
            self.graph.add_node(
                Node(
                    key=key,
                    object_id=rel,
                    object_type=object_type,
                    path=rel,
                    generated=generated,
                    defined=True,
                    details={"docs_relative_path": docs_rel},
                ),
                aliases=(docs_rel,),
            )

    def _file_node(self, path: Path) -> str:
        rel = path.relative_to(self.graph.repo_root).as_posix()
        key = f"file:{rel}"
        if key not in self.graph.nodes:
            raise ImpactError(f"Internal file-node resolution failed for {rel}.")
        return key

    def _index_markdown(self, path: Path) -> None:
        rel = path.relative_to(self.graph.repo_root).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            self.graph.diagnostics.append(
                Diagnostic(
                    code="MARKDOWN_DECODE_ERROR",
                    severity=Severity.ERROR,
                    message=str(exc),
                    path=rel,
                )
            )
            return

        match = DOC_META_PATTERN.search(text)
        if not match:
            return

        try:
            metadata = json.loads(match.group(1))
        except json.JSONDecodeError as exc:
            self.graph.diagnostics.append(
                Diagnostic(
                    code="MARKDOWN_METADATA_INVALID",
                    severity=Severity.ERROR,
                    message=str(exc),
                    path=rel,
                )
            )
            return

        doc_id = metadata.get("doc_id")
        if not isinstance(doc_id, str) or not looks_like_id(doc_id):
            self.graph.diagnostics.append(
                Diagnostic(
                    code="MARKDOWN_DOC_ID_MISSING",
                    severity=Severity.ERROR,
                    message="Active Markdown metadata requires a valid doc_id.",
                    path=rel,
                )
            )
            return

        old_file_key = self._file_node(path)
        doc_key = self.graph.ensure_identifier(
            doc_id,
            "document",
            defined=True,
            details={"title": first_heading(text)},
        )
        self.graph.add_node(
            Node(
                key=doc_key,
                object_id=doc_id,
                object_type="document",
                path=rel,
                document_class=metadata.get("document_class"),
                layer=metadata.get("layer"),
                status=metadata.get("status"),
                generated=(
                    metadata.get("document_class") in {
                        "generated_markdown",
                        "generated_ai_context",
                    }
                    or rel.startswith("docs/generated/")
                ),
                defined=True,
                details={
                    "title": first_heading(text),
                    "language": metadata.get("language"),
                },
            ),
            aliases=(rel, rel.removeprefix("docs/")),
        )
        self._redirect_file_node(old_file_key, doc_key)

        if metadata.get("status") != "active":
            return

        document_class = metadata.get("document_class")
        canonical_relation = (
            "generated_from"
            if document_class in {"generated_markdown", "generated_ai_context"}
            else "referenced_by"
        )

        list_relations = {
            "decision_ids": "referenced_by",
            "requirement_ids": "referenced_by",
            "exception_ids": "exempts",
            "depends_on": "depended_on_by",
            "canonical_refs": canonical_relation,
        }

        for field, relationship in list_relations.items():
            values = metadata.get(field, [])
            if not isinstance(values, list):
                self.graph.diagnostics.append(
                    Diagnostic(
                        code="MARKDOWN_METADATA_FIELD_INVALID",
                        severity=Severity.ERROR,
                        message=f"{field} must be an array.",
                        path=rel,
                        object_id=doc_id,
                    )
                )
                continue
            for value in values:
                if not isinstance(value, str):
                    continue
                target = self._target_node(value, rel)
                self.graph.add_edge(
                    target,
                    doc_key,
                    relationship,
                    evidence_path=rel,
                    evidence_pointer=f"/{field}",
                )

        lock_ids = metadata.get("lock_ids", [])
        if isinstance(lock_ids, list):
            for value in lock_ids:
                if not isinstance(value, str):
                    continue
                target = self._target_node(value, rel)
                self.graph.add_edge(
                    target,
                    doc_key,
                    "constrains",
                    evidence_path=rel,
                    evidence_pointer="/lock_ids",
                )
                self.graph.add_edge(
                    doc_key,
                    target,
                    "requires_lock_review",
                    evidence_path=rel,
                    evidence_pointer="/lock_ids",
                )

        owner_decision = metadata.get("owner_decision_id")
        if isinstance(owner_decision, str) and looks_like_id(owner_decision):
            decision_key = self.graph.ensure_identifier(
                owner_decision,
                "decision",
                defined=True,
                details={"defined_by_adr": doc_id},
            )
            self.graph.add_edge(
                decision_key,
                doc_key,
                "rationalized_by_adr",
                evidence_path=rel,
                evidence_pointer="/owner_decision_id",
            )
            self.graph.add_edge(
                doc_key,
                decision_key,
                "defines_decision_rationale",
                evidence_path=rel,
                evidence_pointer="/owner_decision_id",
            )

        adr_id = metadata.get("adr_id")
        if isinstance(adr_id, str) and looks_like_id(adr_id):
            self.graph.add_alias(adr_id, doc_key)
            self.graph.nodes[doc_key].details["adr_id"] = adr_id
            self.graph.nodes[doc_key].details["adr_status"] = metadata.get("adr_status")

        supersedes = metadata.get("supersedes", [])
        if isinstance(supersedes, list):
            for value in supersedes:
                if isinstance(value, str) and value:
                    target = self._target_node(value, rel)
                    self.graph.add_edge(
                        target,
                        doc_key,
                        "superseded_by",
                        evidence_path=rel,
                        evidence_pointer="/supersedes",
                    )

        superseded_by = metadata.get("superseded_by")
        if isinstance(superseded_by, str) and superseded_by:
            target = self._target_node(superseded_by, rel)
            self.graph.add_edge(
                doc_key,
                target,
                "superseded_by",
                evidence_path=rel,
                evidence_pointer="/superseded_by",
            )

        for req_match in REQUIREMENT_LINE_PATTERN.finditer(text):
            req_id = req_match.group(1)
            req_key = self.graph.ensure_identifier(
                req_id,
                "requirement",
                defined=True,
                details={
                    "strength": req_match.group(2),
                    "statement": req_match.group(3),
                    "defined_in": doc_id,
                },
            )
            self.graph.add_edge(
                doc_key,
                req_key,
                "defines_requirement",
                evidence_path=rel,
            )
            self.graph.add_edge(
                req_key,
                doc_key,
                "defined_in_document",
                evidence_path=rel,
            )

    def _redirect_file_node(self, old_key: str, new_key: str) -> None:
        if old_key == new_key:
            return
        old_node = self.graph.nodes[old_key]
        if old_node.path:
            self.graph.add_alias(old_node.path, new_key)
            if old_node.path.startswith("docs/"):
                self.graph.add_alias(old_node.path.removeprefix("docs/"), new_key)
        for alias, keys in list(self.graph.aliases.items()):
            if old_key in keys:
                keys.discard(old_key)
                keys.add(new_key)
        self.graph.add_edge(
            new_key,
            old_key,
            "materialized_as_file",
            evidence_path=old_node.path,
        )
        self.graph.add_edge(
            old_key,
            new_key,
            "file_represents_object",
            evidence_path=old_node.path,
        )

    def _index_json(self, path: Path) -> None:
        rel = path.relative_to(self.graph.repo_root).as_posix()
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            self.graph.diagnostics.append(
                Diagnostic(
                    code="JSON_INVALID",
                    severity=Severity.ERROR,
                    message=str(exc),
                    path=rel,
                )
            )
            return

        file_key = self._file_node(path)
        root_identity, _ = identity_from_object(data) if isinstance(data, dict) else (None, None)
        if root_identity:
            root_key = self.graph.ensure_identifier(
                root_identity,
                defined=True,
                details={"defined_in": rel},
            )
            self.graph.add_node(
                Node(
                    key=root_key,
                    object_id=root_identity,
                    object_type=infer_object_type_from_id(root_identity),
                    path=rel,
                    pointer="/",
                    status=data.get("status") if isinstance(data, dict) else None,
                    generated=(
                        rel.startswith("docs/generated/")
                        or (
                            isinstance(data, dict)
                            and data.get("document_class") == "generated_ai_context"
                        )
                    ),
                    defined=True,
                ),
                aliases=(rel, rel.removeprefix("docs/"), f"{rel}#/"),
            )
            self._redirect_file_node(file_key, root_key)
            owner_key = root_key
            file_key = root_key
        else:
            owner_key = file_key

        self._walk_json(
            value=data,
            path=rel,
            pointer="",
            owner_key=owner_key,
            file_key=file_key,
        )

    def _walk_json(
        self,
        *,
        value: Any,
        path: str,
        pointer: str,
        owner_key: str,
        file_key: str,
    ) -> None:
        if isinstance(value, dict):
            identity, identity_key = identity_from_object(value)
            current_owner = owner_key
            if identity:
                object_pointer = pointer or "/"
                current_owner = self.graph.ensure_identifier(
                    identity,
                    defined=True,
                    details={
                        "defined_in": path,
                        "identity_key": identity_key,
                    },
                )
                self.graph.add_node(
                    Node(
                        key=current_owner,
                        object_id=identity,
                        object_type=infer_object_type_from_id(identity),
                        path=path,
                        pointer=object_pointer,
                        status=value.get("status") if isinstance(value.get("status"), str) else None,
                        generated=path.startswith("docs/generated/"),
                        defined=True,
                    ),
                    aliases=(
                        f"{path}#{object_pointer}",
                        f"{path.removeprefix('docs/')}#{object_pointer}",
                    ),
                )
                self.graph.add_edge(
                    file_key,
                    current_owner,
                    "contains",
                    evidence_path=path,
                    evidence_pointer=object_pointer,
                )
                self.graph.add_edge(
                    current_owner,
                    file_key,
                    "included_in",
                    evidence_path=path,
                    evidence_pointer=object_pointer,
                )

            for key, child in value.items():
                child_pointer = f"{pointer}/{json_pointer_escape(str(key))}"
                if key in REFERENCE_KEYS:
                    self._index_reference_value(
                        child,
                        key=key,
                        owner_key=current_owner,
                        path=path,
                        pointer=child_pointer,
                    )
                self._walk_json(
                    value=child,
                    path=path,
                    pointer=child_pointer,
                    owner_key=current_owner,
                    file_key=file_key,
                )
            return

        if isinstance(value, list):
            for index, child in enumerate(value):
                child_pointer = f"{pointer}/{index}"
                self._walk_json(
                    value=child,
                    path=path,
                    pointer=child_pointer,
                    owner_key=owner_key,
                    file_key=file_key,
                )
            return

        if isinstance(value, str):
            self._index_scalar_reference(
                value,
                key=None,
                owner_key=owner_key,
                path=path,
                pointer=pointer or "/",
            )

    def _index_reference_value(
        self,
        value: Any,
        *,
        key: str,
        owner_key: str,
        path: str,
        pointer: str,
    ) -> None:
        relationship, owner_to_target = relationship_for_key(key)
        for scalar in iter_scalar_strings(value):
            target = self._target_node(scalar, path)
            if owner_to_target:
                source_key, target_key = owner_key, target
            else:
                source_key, target_key = target, owner_key
            self.graph.add_edge(
                source_key,
                target_key,
                relationship,
                evidence_path=path,
                evidence_pointer=pointer,
            )

    def _index_scalar_reference(
        self,
        value: str,
        *,
        key: str | None,
        owner_key: str,
        path: str,
        pointer: str,
    ) -> None:
        candidate = value.strip()
        if not candidate:
            return
        if not looks_like_id(candidate) and not looks_like_path(candidate):
            return
        if key in REFERENCE_KEYS:
            return
        target = self._target_node(candidate, path)
        self.graph.add_edge(
            target,
            owner_key,
            "referenced_by",
            evidence_path=path,
            evidence_pointer=pointer,
        )

    def _target_node(self, value: str, current_path: str) -> str:
        candidate = value.strip()
        if looks_like_id(candidate):
            return self.graph.ensure_identifier(candidate)
        return self.graph.ensure_reference(candidate, current_path)


def first_heading(text: str) -> str | None:
    match = re.search(r"^# (.+)$", text, re.MULTILINE)
    return match.group(1).strip() if match else None


def discover_repo_root(script_path: Path) -> Path:
    candidate = script_path.resolve().parents[2]
    if (candidate / "docs").is_dir():
        return candidate
    return Path.cwd().resolve()


def run_git(
    repo_root: Path,
    arguments: Sequence[str],
    *,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo_root), *arguments],
        check=check,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def git_available(repo_root: Path) -> bool:
    try:
        result = run_git(repo_root, ["rev-parse", "--is-inside-work-tree"])
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False
    return result.stdout.strip() == "true"


def discover_git_changes(
    repo_root: Path,
    *,
    base_ref: str | None,
    head_ref: str,
    staged: bool,
    include_untracked: bool,
) -> list[str]:
    if not git_available(repo_root):
        return []

    if base_ref:
        arguments = [
            "diff",
            "--name-only",
            "--diff-filter=ACMR",
            f"{base_ref}...{head_ref}",
        ]
    elif staged:
        arguments = ["diff", "--cached", "--name-only", "--diff-filter=ACMR"]
    else:
        arguments = ["diff", "HEAD", "--name-only", "--diff-filter=ACMR"]

    result = run_git(repo_root, arguments)
    paths = {line.strip() for line in result.stdout.splitlines() if line.strip()}

    if include_untracked and not base_ref:
        untracked = run_git(
            repo_root,
            ["ls-files", "--others", "--exclude-standard"],
        )
        paths.update(
            line.strip() for line in untracked.stdout.splitlines() if line.strip()
        )

    return sorted(path for path in paths if path == "docs" or path.startswith("docs/"))


def load_dispositions(path: Path | None) -> dict[str, Disposition]:
    if path is None:
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ImpactError(f"Cannot load dispositions from {path}: {exc}") from exc

    if isinstance(data, dict) and isinstance(data.get("dispositions"), list):
        records = data["dispositions"]
    elif isinstance(data, dict):
        records = [
            {"object_id": object_id, **value}
            for object_id, value in data.items()
            if isinstance(value, dict)
        ]
    else:
        raise ImpactError(
            "Disposition file must be an object or contain a dispositions array."
        )

    result: dict[str, Disposition] = {}
    for record in records:
        if not isinstance(record, dict):
            raise ImpactError("Every disposition entry must be an object.")
        object_id = record.get("object_id")
        disposition_name = record.get("disposition")
        if not isinstance(object_id, str) or not isinstance(disposition_name, str):
            raise ImpactError(
                "Every disposition entry requires string object_id and disposition."
            )
        disposition = Disposition(
            disposition=disposition_name,
            reviewer=record.get("reviewer"),
            reviewed_on=record.get("reviewed_on"),
            rationale=record.get("rationale"),
            exception_id=record.get("exception_id"),
            blocker=record.get("blocker"),
        )
        disposition.validate(object_id)
        result[object_id] = disposition
    return result


def sanitize_identifier(value: str) -> str:
    normalized = re.sub(r"[^A-Za-z0-9-]+", "-", value.strip()).strip("-")
    normalized = re.sub(r"-{2,}", "-", normalized)
    return normalized.upper() or "AUTO"


def current_date(timezone_name: str) -> str:
    try:
        from zoneinfo import ZoneInfo

        return dt.datetime.now(ZoneInfo(timezone_name)).date().isoformat()
    except Exception:
        return dt.date.today().isoformat()


def choose_change_id(
    explicit: str | None,
    object_ids: Sequence[str],
    decision_ids: Sequence[str],
    paths: Sequence[str],
    today: str,
) -> str:
    if explicit:
        return explicit
    if len(decision_ids) == 1:
        return f"CHG-{decision_ids[0]}"
    if len(object_ids) == 1:
        return f"CHG-{object_ids[0]}"
    if len(paths) == 1:
        stem = PurePosixPath(paths[0]).stem
        return f"CHG-{today.replace('-', '')}-{sanitize_identifier(stem)}"
    return f"CHG-AUTO-{today.replace('-', '')}"


def seed_targets_from_arguments(
    graph: ImpactGraph,
    *,
    paths: Sequence[str],
    pointers: Sequence[str],
    object_ids: Sequence[str],
    decision_ids: Sequence[str],
) -> tuple[list[str], list[dict[str, str]]]:
    seeds: list[str] = []
    unresolved: list[dict[str, str]] = []

    def add_alias_target(kind: str, requested: str) -> None:
        normalized = requested.strip().replace("\\", "/")
        matches = graph.resolve_alias(normalized)

        if not matches and kind == "path":
            path_part, _ = split_reference(normalized)
            prefix = path_part.rstrip("/") + "/"
            directory_matches = sorted(
                {
                    key
                    for alias, keys in graph.aliases.items()
                    if (
                        alias == path_part
                        or alias.startswith(prefix)
                        or alias == f"docs/{path_part}"
                        or alias.startswith(f"docs/{prefix}")
                    )
                    for key in keys
                    if graph.nodes[key].path
                }
            )
            matches = directory_matches

        if not matches and looks_like_id(normalized):
            matches = graph.resolve_alias(normalized)

        if not matches:
            unresolved.append({"kind": kind, "target": requested})
            return

        for key in matches:
            if key not in seeds:
                seeds.append(key)

    for path in paths:
        add_alias_target("path", path)
    for pointer in pointers:
        add_alias_target("pointer", pointer)
    for object_id in object_ids:
        add_alias_target("object_id", object_id)
    for decision_id in decision_ids:
        add_alias_target("decision_id", decision_id)

    return seeds, unresolved


def default_disposition(
    node: Node,
    *,
    is_seed: bool,
) -> Disposition:
    if is_seed:
        return Disposition(disposition="updated")
    if node.generated or (
        node.path is not None and node.path.startswith("docs/generated/")
    ):
        return Disposition(disposition="regenerated")
    if node.object_type in {"generated_file", "ai_context"}:
        return Disposition(disposition="regenerated")
    return Disposition(
        disposition="blocked",
        blocker="impact_review_and_explicit_disposition_required",
    )


def disposition_for_node(
    node: Node,
    overrides: Mapping[str, Disposition],
    *,
    is_seed: bool,
) -> Disposition:
    candidate_keys = [
        node.object_id,
        node.path or "",
        f"{node.path}#{node.pointer}" if node.path and node.pointer else "",
        node.key,
    ]
    for key in candidate_keys:
        if key and key in overrides:
            disposition = overrides[key]
            disposition.validate(node.object_id)
            return disposition
    disposition = default_disposition(node, is_seed=is_seed)
    disposition.validate(node.object_id)
    return disposition


def reconstruct_path(
    graph: ImpactGraph,
    records: Mapping[str, TraversalRecord],
    node_key: str,
) -> list[dict[str, Any]]:
    chain: list[dict[str, Any]] = []
    current = node_key
    while True:
        record = records[current]
        if record.predecessor is None or record.edge is None:
            break
        chain.append(record.edge.as_dict(graph))
        current = record.predecessor
    chain.reverse()
    return chain


def accepted_adr_for_decision(graph: ImpactGraph, decision_id: str) -> bool:
    decision_keys = graph.resolve_alias(decision_id)
    for decision_key in decision_keys:
        for edge in graph.edges.get(decision_key, []):
            target = graph.nodes[edge.target]
            if (
                edge.relationship == "rationalized_by_adr"
                and target.document_class == "architecture_decision_record"
                and target.details.get("adr_status") == "accepted"
            ):
                return True
    return False


def build_report(
    graph: ImpactGraph,
    *,
    change_id: str,
    semantic_class: str,
    decision_ids: Sequence[str],
    canonical_targets: list[dict[str, str]],
    seed_keys: Sequence[str],
    records: Mapping[str, TraversalRecord],
    disposition_overrides: Mapping[str, Disposition],
    unresolved_targets: list[dict[str, str]],
    max_depth: int | None,
) -> dict[str, Any]:
    today = current_date(os.environ.get("KOA_TIMEZONE", "America/Montreal"))
    impact_id = f"IMPACT-{today}-{sanitize_identifier(change_id)}"
    seed_set = set(seed_keys)

    affected_objects: list[dict[str, Any]] = []
    blocking_objects: list[str] = []

    ordered_records = sorted(
        records.values(),
        key=lambda record: (
            record.distance,
            graph.nodes[record.node_key].object_type,
            graph.nodes[record.node_key].object_id,
        ),
    )

    for record in ordered_records:
        node = graph.nodes[record.node_key]
        disposition = disposition_for_node(
            node,
            disposition_overrides,
            is_seed=record.node_key in seed_set,
        )
        if disposition.disposition == "blocked":
            blocking_objects.append(node.object_id)

        impact_class = (
            "changed_target"
            if record.distance == 0
            else "direct"
            if record.distance == 1
            else "transitive"
        )
        item = {
            **node.as_dict(),
            "impact_class": impact_class,
            "graph_distance": record.distance,
            "seed_object_id": graph.nodes[record.seed].object_id,
            "relationship_path": reconstruct_path(graph, records, record.node_key),
            "disposition": disposition.as_dict(),
        }
        affected_objects.append(item)

    unresolved_dependencies = []
    for node in graph.unresolved_nodes():
        if node.key in records:
            unresolved_dependencies.append(node.as_dict())

    decision_checks = []
    for decision_id in sorted(set(decision_ids)):
        decision_checks.append(
            {
                "decision_id": decision_id,
                "accepted_adr_present": accepted_adr_for_decision(graph, decision_id),
            }
        )

    activation_blockers: list[dict[str, Any]] = []
    if semantic_class == "unclassified":
        activation_blockers.append(
            {
                "code": "CHANGE_CLASS_UNCLASSIFIED",
                "message": "Select patch, minor, or major before activation.",
            }
        )
    if unresolved_targets:
        activation_blockers.append(
            {
                "code": "UNRESOLVED_CANONICAL_TARGETS",
                "message": "One or more requested canonical targets could not be resolved.",
                "targets": unresolved_targets,
            }
        )
    if unresolved_dependencies:
        activation_blockers.append(
            {
                "code": "UNRESOLVED_DEPENDENCIES",
                "message": (
                    "The affected subgraph includes references whose active canonical "
                    "definitions are not present in the indexed corpus."
                ),
                "count": len(unresolved_dependencies),
            }
        )
    if blocking_objects:
        activation_blockers.append(
            {
                "code": "BLOCKED_DISPOSITIONS",
                "message": "Affected objects still require review or authority.",
                "count": len(blocking_objects),
            }
        )
    if semantic_class == "major":
        if not decision_checks:
            activation_blockers.append(
                {
                    "code": "MAJOR_CHANGE_WITHOUT_DECISION",
                    "message": "A major change requires at least one accepted owner decision.",
                }
            )
        missing_adrs = [
            item["decision_id"]
            for item in decision_checks
            if not item["accepted_adr_present"]
        ]
        if missing_adrs:
            activation_blockers.append(
                {
                    "code": "MAJOR_CHANGE_WITHOUT_ACCEPTED_ADR",
                    "message": "Major decision changes require accepted ADR coverage.",
                    "decision_ids": missing_adrs,
                }
            )

    schema_path = graph.docs_root / "schemas/impact-report.schema.json"

    report = {
        "schema_ref": "schemas/impact-report.schema.json",
        "schema_available": schema_path.exists(),
        "impact_id": impact_id,
        "change_id": change_id,
        "change_class": semantic_class,
        "status": "blocked" if activation_blockers else "complete",
        "generated_on": today,
        "generator": {
            "tool": "docs/tools/compute_impact.py",
            "version": "1.0.0",
            "source_mode": "active_docs_graph",
            "max_depth": max_depth,
            "integrity_policy": (
                "No generic source, metadata, or generated-prose hash is recorded."
            ),
        },
        "decision_ids": sorted(set(decision_ids)),
        "decision_checks": decision_checks,
        "canonical_targets": canonical_targets,
        "graph_summary": graph.graph_summary(),
        "impact_summary": {
            "changed_targets": sum(
                1 for item in affected_objects if item["impact_class"] == "changed_target"
            ),
            "direct_objects": sum(
                1 for item in affected_objects if item["impact_class"] == "direct"
            ),
            "transitive_objects": sum(
                1 for item in affected_objects if item["impact_class"] == "transitive"
            ),
            "affected_objects": len(affected_objects),
            "blocked_dispositions": len(blocking_objects),
            "unresolved_targets": len(unresolved_targets),
            "unresolved_dependencies": len(unresolved_dependencies),
        },
        "affected_objects": affected_objects,
        "unresolved_targets": unresolved_targets,
        "unresolved_dependencies": unresolved_dependencies,
        "diagnostics": [item.as_dict() for item in graph.diagnostics],
        "activation": {
            "eligible": not activation_blockers,
            "blockers": activation_blockers,
        },
    }
    return report


def write_report(report: Mapping[str, Any], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = output_path.with_name(f".{output_path.name}.tmp")
    temporary.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, output_path)


def print_summary(report: Mapping[str, Any], *, output_path: Path | None) -> None:
    summary = report["impact_summary"]
    print(
        f"{report['impact_id']}: {summary['affected_objects']} affected "
        f"({summary['changed_targets']} changed, {summary['direct_objects']} direct, "
        f"{summary['transitive_objects']} transitive); "
        f"{summary['blocked_dispositions']} blocked dispositions; "
        f"activation eligible={str(report['activation']['eligible']).lower()}."
    )
    if output_path is not None:
        print(output_path.as_posix())
    if report["unresolved_targets"]:
        print(
            f"Unresolved requested targets: {len(report['unresolved_targets'])}.",
            file=sys.stderr,
        )
    if report["unresolved_dependencies"]:
        print(
            f"Unresolved affected dependencies: "
            f"{len(report['unresolved_dependencies'])}.",
            file=sys.stderr,
        )


def graph_validation_exit_code(graph: ImpactGraph, *, strict: bool) -> int:
    errors = [
        diagnostic
        for diagnostic in graph.diagnostics
        if diagnostic.severity == Severity.ERROR
    ]
    if errors:
        return 2
    if strict and graph.unresolved_nodes():
        return 1
    return 0


def run_self_test() -> int:
    with tempfile.TemporaryDirectory(prefix="koa-impact-self-test-") as tmp:
        repo_root = Path(tmp)
        docs_root = repo_root / "docs"
        (docs_root / "10-adrs").mkdir(parents=True)
        (docs_root / "02-system").mkdir(parents=True)
        (docs_root / "generated").mkdir(parents=True)

        adr_meta = {
            "doc_id": "DOC-ADR-900",
            "document_class": "architecture_decision_record",
            "status": "active",
            "language": "en",
            "layer": "adrs",
            "adr_id": "ADR-900",
            "adr_status": "accepted",
            "owner_decision_id": "DEC-TEST-900",
            "decision_ids": ["DEC-TEST-900"],
            "requirement_ids": [],
            "lock_ids": [],
            "exception_ids": [],
            "depends_on": [],
            "canonical_refs": [],
        }
        adr_text = (
            "<!-- KOA:DOC-META:BEGIN GENERATED\n"
            + json.dumps(adr_meta, indent=2)
            + "\nKOA:DOC-META:END -->\n\n"
            "# ADR-900 — Test\n"
        )
        (docs_root / "10-adrs/ADR-900-test.md").write_text(
            adr_text,
            encoding="utf-8",
        )

        system_meta = {
            "doc_id": "DOC-SYS-900",
            "document_class": "normative_markdown",
            "status": "active",
            "language": "en",
            "layer": "system",
            "decision_ids": ["DEC-TEST-900"],
            "requirement_ids": ["REQ-TEST-900"],
            "lock_ids": ["LOCK-TEST-900"],
            "exception_ids": [],
            "depends_on": ["DOC-ADR-900"],
            "canonical_refs": [],
        }
        system_text = (
            "<!-- KOA:DOC-META:BEGIN GENERATED\n"
            + json.dumps(system_meta, indent=2)
            + "\nKOA:DOC-META:END -->\n\n"
            "# Test System\n\n"
            "- **REQ-TEST-900 — SHALL:** Preserve test impact.\n"
        )
        (docs_root / "02-system/test.md").write_text(system_text, encoding="utf-8")

        generated_meta = {
            "doc_id": "DOC-GEN-900",
            "document_class": "generated_markdown",
            "status": "active",
            "language": "en",
            "layer": "generated",
            "decision_ids": ["DEC-TEST-900"],
            "requirement_ids": ["REQ-TEST-900"],
            "lock_ids": [],
            "exception_ids": [],
            "depends_on": ["DOC-SYS-900"],
            "canonical_refs": ["docs/02-system/test.md"],
        }
        generated_text = (
            "<!-- KOA:DOC-META:BEGIN GENERATED\n"
            + json.dumps(generated_meta, indent=2)
            + "\nKOA:DOC-META:END -->\n\n"
            "# Generated Test\n"
        )
        (docs_root / "generated/test.md").write_text(
            generated_text,
            encoding="utf-8",
        )

        graph = ImpactGraph(repo_root=repo_root, docs_root=docs_root)
        CorpusIndexer(graph).build()
        seeds, unresolved = seed_targets_from_arguments(
            graph,
            paths=[],
            pointers=[],
            object_ids=[],
            decision_ids=["DEC-TEST-900"],
        )
        if unresolved or len(seeds) != 1:
            raise AssertionError("Self-test failed to resolve decision seed.")
        records = graph.traverse(seeds, max_depth=None)

        impacted_ids = {graph.nodes[key].object_id for key in records}
        required = {
            "DEC-TEST-900",
            "DOC-ADR-900",
            "DOC-SYS-900",
            "REQ-TEST-900",
            "LOCK-TEST-900",
            "DOC-GEN-900",
        }
        if not required.issubset(impacted_ids):
            missing = sorted(required - impacted_ids)
            raise AssertionError(f"Self-test missing impact nodes: {missing}")

        if not accepted_adr_for_decision(graph, "DEC-TEST-900"):
            raise AssertionError("Self-test did not resolve accepted ADR.")

    print("compute_impact.py self-test: pass")
    return 0


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Compute direct and transitive kOA documentation impact from active "
            "Markdown metadata and JSON contracts."
        )
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        help="Repository root. Defaults to the repository containing this script.",
    )
    parser.add_argument(
        "--docs-root",
        type=Path,
        help="Documentation root. Defaults to <repo-root>/docs.",
    )
    parser.add_argument("--change-id", help="Stable CHG-ID or other change identifier.")
    parser.add_argument(
        "--semantic-class",
        choices=sorted(SEMANTIC_CLASSES),
        default="unclassified",
        help="Semantic change class. Defaults to unclassified and blocks activation.",
    )
    parser.add_argument(
        "--path",
        action="append",
        default=[],
        help="Changed repo-relative path or docs-relative path. Repeatable.",
    )
    parser.add_argument(
        "--pointer",
        action="append",
        default=[],
        help="Changed path plus JSON Pointer, for example contracts/x.json#/items/0.",
    )
    parser.add_argument(
        "--object-id",
        action="append",
        default=[],
        help="Changed canonical object ID. Repeatable.",
    )
    parser.add_argument(
        "--decision-id",
        action="append",
        default=[],
        help="Accepted owner decision ID associated with the change. Repeatable.",
    )
    parser.add_argument(
        "--base-ref",
        help="Discover changed docs with git diff <base-ref>...<head-ref>.",
    )
    parser.add_argument(
        "--head-ref",
        default="HEAD",
        help="Git head ref used with --base-ref. Defaults to HEAD.",
    )
    parser.add_argument(
        "--staged",
        action="store_true",
        help="Discover only staged changes when no --base-ref is supplied.",
    )
    parser.add_argument(
        "--no-untracked",
        action="store_true",
        help="Exclude untracked documentation files from Git discovery.",
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        help="Maximum transitive graph distance. Omit for complete traversal.",
    )
    parser.add_argument(
        "--dispositions",
        type=Path,
        help="JSON file containing reviewed disposition overrides.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help=(
            "Output JSON path. Defaults to "
            "docs/generated/impact/IMPACT-<date>-<change-id>.json."
        ),
    )
    parser.add_argument(
        "--json-stdout",
        action="store_true",
        help="Print the complete report as JSON instead of writing it.",
    )
    parser.add_argument(
        "--check-clean",
        action="store_true",
        help=(
            "Read-only validation mode. Discover Git changes when possible, "
            "compute impact, and do not write a report."
        ),
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat unresolved canonical references as validation failures.",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run the built-in isolated graph test and exit.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_argument_parser()
    args = parser.parse_args(argv)

    if args.self_test:
        return run_self_test()

    script_path = Path(__file__)
    repo_root = (args.repo_root or discover_repo_root(script_path)).resolve()
    docs_root = (args.docs_root or repo_root / "docs").resolve()

    if not docs_root.is_dir():
        parser.error(f"Documentation root does not exist: {docs_root}")
    try:
        docs_root.relative_to(repo_root)
    except ValueError:
        parser.error("Documentation root must be inside the repository root.")

    if args.max_depth is not None and args.max_depth < 0:
        parser.error("--max-depth must be zero or greater.")

    graph = ImpactGraph(repo_root=repo_root, docs_root=docs_root)
    try:
        CorpusIndexer(graph).build()
    except ImpactError as exc:
        print(f"impact-error: {exc}", file=sys.stderr)
        return 2

    explicit_paths = list(args.path)
    git_paths: list[str] = []
    if not (
        args.path
        or args.pointer
        or args.object_id
        or args.decision_id
    ):
        git_paths = discover_git_changes(
            repo_root,
            base_ref=args.base_ref,
            head_ref=args.head_ref,
            staged=args.staged,
            include_untracked=not args.no_untracked,
        )
        explicit_paths.extend(git_paths)

    seeds, unresolved_targets = seed_targets_from_arguments(
        graph,
        paths=explicit_paths,
        pointers=args.pointer,
        object_ids=args.object_id,
        decision_ids=args.decision_id,
    )

    if not seeds:
        exit_code = graph_validation_exit_code(graph, strict=args.strict)
        summary = graph.graph_summary()
        print(
            "Impact graph validated: "
            f"{summary['node_count']} nodes, {summary['edge_count']} edges, "
            f"{summary['unresolved_node_count']} unresolved references."
        )
        if unresolved_targets:
            print(
                json.dumps(
                    {"unresolved_targets": unresolved_targets},
                    indent=2,
                    ensure_ascii=False,
                ),
                file=sys.stderr,
            )
            return 2
        return exit_code

    records = graph.traverse(seeds, args.max_depth)

    today = current_date(os.environ.get("KOA_TIMEZONE", "America/Montreal"))
    change_id = choose_change_id(
        args.change_id,
        args.object_id,
        args.decision_id,
        explicit_paths,
        today,
    )

    canonical_targets = (
        [{"kind": "path", "target": value} for value in explicit_paths]
        + [{"kind": "pointer", "target": value} for value in args.pointer]
        + [{"kind": "object_id", "target": value} for value in args.object_id]
        + [{"kind": "decision_id", "target": value} for value in args.decision_id]
    )

    try:
        disposition_overrides = load_dispositions(args.dispositions)
        report = build_report(
            graph,
            change_id=change_id,
            semantic_class=args.semantic_class,
            decision_ids=args.decision_id,
            canonical_targets=canonical_targets,
            seed_keys=seeds,
            records=records,
            disposition_overrides=disposition_overrides,
            unresolved_targets=unresolved_targets,
            max_depth=args.max_depth,
        )
    except ImpactError as exc:
        print(f"impact-error: {exc}", file=sys.stderr)
        return 2

    if args.json_stdout:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        output_path = None
    elif args.check_clean:
        output_path = None
        print_summary(report, output_path=None)
    else:
        if args.output:
            output_path = args.output
            if not output_path.is_absolute():
                output_path = repo_root / output_path
        else:
            output_path = (
                docs_root
                / "generated"
                / "impact"
                / f"{report['impact_id']}.json"
            )
        write_report(report, output_path)
        print_summary(report, output_path=output_path)

    parse_errors = [
        item
        for item in graph.diagnostics
        if item.severity == Severity.ERROR
    ]
    if parse_errors or unresolved_targets:
        return 2
    if args.strict and report["unresolved_dependencies"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
