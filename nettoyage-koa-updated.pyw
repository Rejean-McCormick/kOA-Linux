from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path
from tkinter import messagebox

REPO_ROOT = Path(r"C:\mycode\kOA-Linux\koa-linux")

PATHS_TO_REMOVE = (
    "GitSink.bat",
    "_delivery",
    "koa-pipeline-diag-20260827_160217",
    "koa-pipeline-diag-20260827_160217.zip",
    "pipeline-plan-diag-20260828_065211.zip",
    "profile-levelup-diag.txt",
    "profile-schema-authority-diag.txt",
    "components/resource-governor/build",
    "components/resource-governor/src/koa_resource_governor.egg-info",
    "generated/profiles/sovereign_linux_node/effective-profile.json",
)


def run(cmd: list[str], *, required: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )

    if required and result.returncode != 0:
        details = (result.stderr or result.stdout or "Erreur inconnue").strip()
        raise RuntimeError(
            f"Commande échouée :\n{' '.join(cmd)}\n\n{details[-2200:]}"
        )

    return result


def remove_path(relative: str) -> None:
    run(
        ["git", "rm", "-r", "-f", "--ignore-unmatch", "--", relative],
        required=False,
    )

    target = REPO_ROOT / relative
    if target.is_dir():
        shutil.rmtree(target)
    elif target.exists():
        target.unlink()


def main() -> None:
    global REPO_ROOT

    if len(sys.argv) > 1:
        REPO_ROOT = Path(sys.argv[1]).resolve()

    if not REPO_ROOT.is_dir():
        messagebox.showerror(
            "Nettoyage kOA",
            f"Dépôt introuvable :\n{REPO_ROOT}",
        )
        return

    try:
        for relative in PATHS_TO_REMOVE:
            remove_path(relative)

        # Régénère les index/documentation.
        run([
            "uv", "run", "--frozen", "python",
            "docs/tools/build_indexes.py",
        ])

        # Régénère le contexte IA et les fichiers subsystem/koa-navigation.
        run([
            "uv", "run", "--frozen", "python",
            "docs/tools/build_ai_context.py",
        ])

        # Vérifie immédiatement que le contenu généré est à jour.
        run([
            "uv", "run", "--frozen", "python",
            "docs/tools/check_generated_content.py",
        ])

        messagebox.showinfo(
            "Nettoyage kOA",
            "Nettoyage terminé.\n\n"
            "Les résidus ont été supprimés et tout le contenu généré a été régénéré.\n"
            "check_generated_content.py : PASS\n\n"
            "Relance maintenant le diagnostic depuis le Control Panel.",
        )

    except Exception as exc:
        messagebox.showerror("Nettoyage kOA", str(exc))


if __name__ == "__main__":
    main()
