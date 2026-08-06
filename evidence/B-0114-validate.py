from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

EXPECTED = {
    ".github/workflows/components.yml",
    ".github/workflows/contracts.yml",
    ".github/workflows/documentation.yml",
    "ci/README.md",
    "ci/policies/path-filters.json",
    "ci/policies/required-checks.json",
}
CHECKS = {"documentation", "contracts", "components"}
ARCH_DOCS = [
    "docs/02-system/code-and-filesystem-architecture/24-repository-root-and-documentation.md",
    "docs/02-system/code-and-filesystem-architecture/25-internal-components-node-trust-governance.md",
    "docs/02-system/code-and-filesystem-architecture/26-internal-components-data-publication-and-knowledge.md",
    "docs/02-system/code-and-filesystem-architecture/27-independent-subsystem-integrations.md",
    "docs/02-system/code-and-filesystem-architecture/28-uckk-external-services-and-transport-interfaces.md",
    "docs/02-system/code-and-filesystem-architecture/29-host-platform-files.md",
    "docs/02-system/code-and-filesystem-architecture/30-assembly-profiles-packaging-and-release.md",
    "docs/02-system/code-and-filesystem-architecture/31-operations-tests-tools-development-and-ci.md",
]

class UniqueKeyLoader(yaml.SafeLoader):
    pass

def construct_mapping(loader: UniqueKeyLoader, node: yaml.Node, deep: bool = False) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(f"duplicate YAML key: {key!r}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping

UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping)


def fail(message: str) -> None:
    raise AssertionError(message)


def inventory_paths(docs_root: Path) -> list[str]:
    items: list[str] = []
    for rel in ARCH_DOCS:
        path = docs_root / rel
        if not path.is_file():
            fail(f"missing architecture source: {rel}")
        in_block = False
        for line in path.read_text(encoding="utf-8").splitlines():
            value = line.strip()
            if value.startswith("```"):
                in_block = not in_block
                continue
            if (
                not in_block
                or not value
                or " " in value
                or value.endswith("/")
                or any(char in value for char in "├└│")
            ):
                continue
            if "/" in value or value.startswith(".") or re.match(r"^[\w-]+(?:\.[\w-]+)+$", value):
                items.append(value)
    if len(items) != 1040 or len(set(items)) != 1040:
        fail(f"expected 1040 unique inventory paths, got {len(items)} / {len(set(items))}")
    return sorted(items)


def argv_to_command(argv: list[str]) -> str:
    if not argv or any(not isinstance(item, str) or not item for item in argv):
        fail(f"invalid command argv: {argv!r}")
    if any(re.search(r"[\n\r\x00]", item) for item in argv):
        fail(f"unsafe command argv: {argv!r}")
    return " ".join(argv)


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: B-0114-validate.py WORKTREE DOCS_EXTRACT", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    docs_extract = Path(sys.argv[2]).resolve()

    actual = {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file() and ".git" not in path.relative_to(root).parts
    }
    if actual != EXPECTED:
        fail(f"allowlist mismatch: missing={sorted(EXPECTED-actual)} extra={sorted(actual-EXPECTED)}")

    for rel in sorted(EXPECTED):
        text = (root / rel).read_text(encoding="utf-8")
        if not text.endswith("\n"):
            fail(f"missing final newline: {rel}")
        if re.search(r"\b(?:TODO|FIXME|XXX)\b", text, flags=re.I):
            fail(f"unresolved marker in {rel}")

    policies: dict[str, dict[str, Any]] = {}
    for name in ("required-checks.json", "path-filters.json"):
        path = root / "ci/policies" / name
        data = json.loads(path.read_text(encoding="utf-8"))
        canonical = json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        if path.read_text(encoding="utf-8") != canonical:
            fail(f"non-canonical JSON ordering: {path}")
        policies[name] = data

    required = policies["required-checks.json"]
    filters = policies["path-filters.json"]
    if required.get("policy_id") != "koa.required-checks" or required.get("status") != "active":
        fail("invalid required-checks identity/status")
    if filters.get("policy_id") != "koa.path-filters" or filters.get("status") != "active":
        fail("invalid path-filters identity/status")

    checks = required.get("checks")
    if not isinstance(checks, list) or {item.get("check_id") for item in checks} != CHECKS:
        fail("required check set must be exactly documentation/contracts/components")
    if len({item.get("required_context") for item in checks}) != 3:
        fail("required contexts must be unique")
    execution = required.get("execution_policy", {})
    if execution.get("all_checks_always_report") is not True:
        fail("all required checks must always report")
    for key in ("blocked_is_success", "cancelled_is_success", "failure_is_success", "neutral_is_success", "skipped_is_success", "timed_out_is_success"):
        if execution.get(key) is not False:
            fail(f"{key} must be false")
    if execution.get("accepted_conclusions") != ["success"]:
        fail("only success may satisfy a required check")
    if execution.get("dependency_installation") != ["uv", "sync", "--frozen", "--all-groups"]:
        fail("dependency synchronization must match the UV toolchain contract")

    workflows: dict[str, dict[str, Any]] = {}
    for item in checks:
        workflow_path = root / item["workflow_file"]
        data = yaml.load(workflow_path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
        if not isinstance(data, dict):
            fail(f"workflow root is not an object: {workflow_path}")
        workflows[item["check_id"]] = data
        if data.get("name") != item["workflow_name"]:
            fail(f"workflow name drift: {workflow_path}")
        events = data.get("on")
        if not isinstance(events, dict):
            fail(f"workflow events missing: {workflow_path}")
        if set(events) != {"merge_group", "pull_request", "push", "workflow_dispatch"}:
            fail(f"unexpected event set in {workflow_path}: {set(events)}")
        serialized_events = json.dumps(events, sort_keys=True)
        if "paths" in serialized_events or "paths-ignore" in serialized_events:
            fail(f"required workflow may not use path trigger filters: {workflow_path}")
        if "pull_request_target" in events:
            fail(f"pull_request_target prohibited: {workflow_path}")
        if data.get("permissions") != {"contents": "read"}:
            fail(f"workflow permissions must be read-only: {workflow_path}")
        jobs = data.get("jobs")
        if not isinstance(jobs, dict) or set(jobs) != {item["job_id"]}:
            fail(f"workflow must contain exactly its stable job: {workflow_path}")
        job = jobs[item["job_id"]]
        if job.get("name") != item["job_name"]:
            fail(f"job name drift: {workflow_path}")
        if job.get("runs-on") != "ubuntu-24.04":
            fail(f"worker identity must be explicit: {workflow_path}")
        timeout = job.get("timeout-minutes")
        if not isinstance(timeout, int) or not (1 <= timeout <= 60):
            fail(f"invalid timeout: {workflow_path}")
        steps = job.get("steps")
        if not isinstance(steps, list) or len(steps) != 4:
            fail(f"workflow must remain a four-step thin orchestrator: {workflow_path}")
        if steps[0].get("uses") != "actions/checkout@v4" or steps[0].get("with", {}).get("persist-credentials") is not False:
            fail(f"checkout must disable persisted credentials: {workflow_path}")
        if steps[1].get("uses") != "astral-sh/setup-uv@v6" or steps[1].get("with", {}).get("enable-cache") is not False:
            fail(f"UV setup must disable cache: {workflow_path}")
        run_commands = [step.get("run") for step in steps if "run" in step]
        expected_commands = [argv_to_command(argv) for argv in item["local_commands"]]
        if run_commands != expected_commands:
            fail(f"workflow/local command drift in {workflow_path}: {run_commands!r} != {expected_commands!r}")
        for command in run_commands:
            if "\n" in command or any(token in command for token in ("curl ", "wget ", "sudo ", "docker ", "git push", "release", "sign")):
                fail(f"workflow contains non-thin or prohibited command: {workflow_path}: {command}")
        raw = workflow_path.read_text(encoding="utf-8")
        if "secrets." in raw or "permissions: write" in raw:
            fail(f"workflow may not consume secrets or write permissions: {workflow_path}")

    readme = (root / "ci/README.md").read_text(encoding="utf-8")
    for item in checks:
        for argv in item["local_commands"]:
            command = argv_to_command(argv)
            if command not in readme:
                fail(f"README omits exact local command: {command}")
        if item["required_context"] not in readme:
            fail(f"README omits required context: {item['required_context']}")

    matching = filters.get("matching", {})
    if matching.get("unknown_path_action") != "run_all" or matching.get("default_checks") != ["documentation", "contracts", "components"]:
        fail("unknown paths must fail closed to all checks")
    if matching.get("workflow_trigger_filtering_allowed") is not False:
        fail("path policy may not suppress required workflow emission")
    filter_items = filters.get("filters")
    if not isinstance(filter_items, list) or {item.get("check_id") for item in filter_items} != CHECKS:
        fail("path filter set must match required checks")
    for item in filter_items:
        includes = item.get("include")
        if not isinstance(includes, list) or not includes or len(includes) != len(set(includes)):
            fail(f"invalid or duplicate include patterns for {item.get('check_id')}")
        if item.get("exclude") != []:
            fail("exclusions are prohibited in the baseline policy")

    paths = inventory_paths(docs_extract)
    roots = {path.split("/", 1)[0] if "/" in path else path for path in paths}
    root_map = filters.get("root_coverage", {}).get("root_to_checks")
    if not isinstance(root_map, dict) or set(root_map) != roots:
        fail(f"root coverage mismatch: missing={sorted(roots-set(root_map or {}))} extra={sorted(set(root_map or {})-roots)}")
    for root_name, mapped in root_map.items():
        if not isinstance(mapped, list) or not mapped or not set(mapped) <= CHECKS or len(mapped) != len(set(mapped)):
            fail(f"invalid root mapping for {root_name}: {mapped!r}")
    if filters.get("root_coverage", {}).get("inventory_source") != ARCH_DOCS:
        fail("architecture inventory source list drift")

    for required_global in (
        ".github/**", ".koa/**", "ci/**", "docs/AI_CONTEXT.md",
        "docs/contracts/ai-navigation.contract.json", "docs/contracts/system.contract.json",
        "docs/contracts/terminology.contract.json", "docs/generated/**", "generated/**",
        "pyproject.toml", "tools/**", "uv.lock"
    ):
        if required_global not in filters.get("global_invalidators", []):
            fail(f"global invalidator omitted: {required_global}")

    if not EXPECTED <= set(paths):
        fail(f"bundle paths missing from frozen inventory: {sorted(EXPECTED-set(paths))}")

    print("B-0114 validation: pass")
    print(f"files={len(actual)}; workflows={len(workflows)}; required_checks={len(checks)}; inventory_paths={len(paths)}; roots={len(roots)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
