from __future__ import annotations

from configparser import ConfigParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _unit(relative: str) -> ConfigParser:
    parser = ConfigParser(strict=False, interpolation=None, delimiters=("="), comment_prefixes=("#", ";"))
    parser.optionxform = str
    parser.read_string((ROOT / relative).read_text(encoding="utf-8"))
    return parser


def test_activation_requires_verified_release_and_conflicts_with_recovery() -> None:
    activation = _unit("host/systemd/units/koa-activation.service")
    verification = _unit("host/systemd/units/koa-release-set-verify.service")
    target = _unit("host/systemd/targets/koa-activation.target")

    assert "koa-release-set-verify.service" in activation["Unit"]["Requires"].split()
    assert activation["Unit"]["Conflicts"] == "koa-recovery.target"
    assert target["Unit"]["Conflicts"] == "koa-recovery.target"
    assert "koa-critical.target" in verification["Unit"]["Before"].split()
    assert verification["Service"]["RemainAfterExit"] == "yes"


def test_service_activation_has_no_ambient_or_network_privilege() -> None:
    for relative in (
        "host/systemd/units/koa-activation.service",
        "host/systemd/units/koa-health-aggregate.service",
        "host/systemd/units/koa-backup.service",
    ):
        unit = _unit(relative)
        service = unit["Service"]
        assert service["NoNewPrivileges"] == "yes"
        assert service["PrivateDevices"] == "yes"
        assert service["ProtectSystem"] == "strict"
        assert service["CapabilityBoundingSet"] == ""
        assert service["AmbientCapabilities"] == ""
        assert service["IPAddressDeny"] == "any"
