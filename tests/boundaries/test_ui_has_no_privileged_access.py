from __future__ import annotations

import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UI_MARKERS = {"ui", "frontend", "presentation", "web", "shell", "session", "sidebar", "topbar"}
PRIVILEGED_TEXT = re.compile(
    r"(?:\bsudo\b|\bpkexec\b|\bsystemctl\b|org\.freedesktop\.PolicyKit|"
    r"/run/koa/sockets/(?:koa-)?node-agent|koa_node_agent\.(?:broker|adapters)|subprocess\.(?:run|Popen|call)|os\.system)",
    re.I,
)


def _is_ui_path(path: Path) -> bool:
    lowered = {part.lower().replace("-", "_") for part in path.parts}
    return bool(lowered & UI_MARKERS) or any(marker in path.name.lower() for marker in UI_MARKERS)


def ui_privilege_violations(repository: Path) -> list[str]:
    failures: list[str] = []
    for root_name in ("components", "integrations", "host", "assembly"):
        root = repository / root_name
        if not root.is_dir():
            continue
        for source in sorted(root.rglob("*")):
            if not source.is_file() or source.suffix.lower() not in {".py", ".rs", ".js", ".ts", ".tsx", ".jsx", ".toml"}:
                continue
            if "tests" in source.parts or not _is_ui_path(source.relative_to(repository)):
                continue
            text = source.read_text(encoding="utf-8", errors="replace")
            for match in PRIVILEGED_TEXT.finditer(text):
                failures.append(f"{source.relative_to(repository)} contains privileged access token {match.group(0)!r}")
            if source.suffix == ".py":
                try:
                    tree = ast.parse(text, filename=str(source))
                except SyntaxError:
                    continue
                imports = {
                    alias.name
                    for node in ast.walk(tree)
                    if isinstance(node, ast.Import)
                    for alias in node.names
                }
                if "subprocess" in imports:
                    failures.append(f"{source.relative_to(repository)} imports subprocess from a UI surface")
    return sorted(set(failures))


def test_repository_ui_has_no_direct_privileged_access() -> None:
    assert ui_privilege_violations(ROOT) == []


def test_ui_subprocess_call_is_detected(tmp_path: Path) -> None:
    source = tmp_path / "components" / "shell" / "src" / "ui" / "power.py"
    source.parent.mkdir(parents=True)
    source.write_text('import subprocess\nsubprocess.run(["systemctl", "reboot"])\n', encoding="utf-8")
    failures = ui_privilege_violations(tmp_path)
    assert any("subprocess" in failure for failure in failures)
    assert any("systemctl" in failure for failure in failures)


def test_public_client_call_is_allowed(tmp_path: Path) -> None:
    source = tmp_path / "components" / "shell" / "src" / "ui" / "status.py"
    source.parent.mkdir(parents=True)
    source.write_text("from koa_interfaces import Client\nstatus = Client().health()\n", encoding="utf-8")
    assert ui_privilege_violations(tmp_path) == []
