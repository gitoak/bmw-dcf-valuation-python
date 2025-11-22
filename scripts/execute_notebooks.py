"""Execute every notebook in notebooks/ using nbconvert.

Designed for CI and local smoke tests so we catch runtime regressions early.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NB_DIR = ROOT / "notebooks"


def _run_notebook(notebook: Path) -> None:
    cmd = [
        "jupyter",
        "nbconvert",
        "--to",
        "notebook",
        "--execute",
        "--inplace",
        str(notebook),
    ]
    subprocess.run(cmd, check=True)


def main() -> None:
    notebooks = sorted(NB_DIR.glob("*.ipynb"))
    if not notebooks:
        print("[notebooks] no notebooks found – skipping execution")
        return

    for nb in notebooks:
        print(f"[notebooks] executing {nb.relative_to(ROOT)}")
        _run_notebook(nb)


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:  # pragma: no cover
        print(f"Notebook execution failed with exit code {exc.returncode}", file=sys.stderr)
        raise
