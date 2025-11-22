"""Automation entry points for tests, linting, and notebook smoke runs."""

from __future__ import annotations

from pathlib import Path

try:
    import nox  # type: ignore[import]
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "nox is required for this automation entry-point. Install dev deps via `uv sync`."
    ) from exc

PYTHON_VERSION = "3.12"

nox.options.reuse_existing_virtualenvs = True
nox.options.stop_on_first_error = False
NOTEBOOKS = sorted(Path("notebooks").glob("*.ipynb"))


def _ensure_uv(session: nox.Session) -> None:
    session.install("uv")


def _sync(session: nox.Session) -> None:
    session.run("uv", "sync", "--all-extras", "--dev", external=True)


@nox.session(python=PYTHON_VERSION)
def tests(session: nox.Session) -> None:
    _ensure_uv(session)
    _sync(session)
    session.run("uv", "run", "pytest", external=True)


@nox.session(python=PYTHON_VERSION)
def lint(session: nox.Session) -> None:
    _ensure_uv(session)
    _sync(session)
    session.run("uv", "run", "ruff", "check", ".", external=True)
    session.run("uv", "run", "ruff", "format", "--check", ".", external=True)
    if NOTEBOOKS:
        session.run("uv", "run", "nbqa", "ruff", "--fix", "notebooks", external=True)
    else:
        session.log("No notebooks to lint – skipping nbqa")


@nox.session(python=PYTHON_VERSION)
def notebooks(session: nox.Session) -> None:
    _ensure_uv(session)
    _sync(session)
    if NOTEBOOKS:
        session.run("uv", "run", "python", "scripts/execute_notebooks.py", external=True)
    else:
        session.log("No notebooks to execute – skipping")


@nox.session(python=PYTHON_VERSION)
def qa(session: nox.Session) -> None:
    _ensure_uv(session)
    _sync(session)
    session.run("uv", "run", "ruff", "check", ".", external=True)
    session.run("uv", "run", "ruff", "format", "--check", ".", external=True)
    session.run("uv", "run", "pytest", external=True)
    if NOTEBOOKS:
        session.run("uv", "run", "nbqa", "ruff", "--fix", "notebooks", external=True)
        session.run("uv", "run", "python", "scripts/execute_notebooks.py", external=True)
    else:
        session.log("No notebooks detected – skipping nbqa + execution")
