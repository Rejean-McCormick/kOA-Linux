"""Core package metadata for the kOA repository tooling."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

__all__ = ["__version__"]


def _installed_version() -> str:
    """Return the installed distribution version without inventing one.

    The repository tooling can be executed from an editable checkout before a
    distribution has been installed.  In that case the explicit local-source
    marker keeps ``--version`` deterministic without claiming a release
    version.
    """

    for distribution_name in ("koa-tools", "koa-linux"):
        try:
            return version(distribution_name)
        except PackageNotFoundError:
            continue
    return "0+local-source"


__version__ = _installed_version()
