# Python Data Science Template

Ein modernes, "batteries-included" Template für Data Science Projekte in Python.

## Features

- **Dependency Management**: [uv](https://github.com/astral-sh/uv) installiert ein konsistentes Python-3.12-Environment (`.venv/`).
- **Code Quality**: [Ruff](https://github.com/astral-sh/ruff) für Linting und Formatting.
- **Testing**: [pytest](https://docs.pytest.org/) Setup inklusive.
- **CI/CD**: GitHub Actions Workflow für automatische Tests und Checks.
- **Pre-commit**: Hooks für automatische Code-Qualitäts-Checks vor dem Commit.
- **VS Code**: Vorkonfigurierte Settings und Extensions.
- **Dev Container**: Sofort startklar in GitHub Codespaces oder Docker.
- **Notebook Hygiene**: `nbstripout` hält Outputs sauber, `nbqa` lintet Notebooks, `nox`/`Makefile`-Targets automatisieren den Analyse-Loop.

## Schnellstart

1. **Repository klonen**
   ```bash
   git clone <dein-repo-url>
   cd ds
   ```

2. **Dependencies installieren**
   ```bash
   make install
   # oder
   uv sync
   ```
   > uv legt standardmäßig ein lokales `.venv/` an (siehe `UV_PROJECT_ENVIRONMENT`).

3. **Tests ausführen**
   ```bash
   make test
   ```

4. **Code formatieren & linten**
   ```bash
   make format
   make lint
   ```

5. **Notebook-Loop**
   ```bash
   make notebook        # startet Jupyter Lab in ./notebooks
   make nbqa            # lintet/fixt Notebooks via nbqa + Ruff
   make notebooks-run   # führt alle *.ipynb headless aus
   make nbstripout-install  # installiert Git-Filter zum Entfernen von Outputs
   make qa              # ruft Tests + Lints gebündelt (via nox) auf
   ```

6. **Nox nutzen (optional, CI-ähnlich)**
   ```bash
   uv run nox -s tests        # nur Tests
   uv run nox -s notebooks    # headless Notebook-Lauf
   uv run nox -s qa           # alles zusammen
   ```

Mehr Details findest du in `notebooks/README.md` und `data/README.md` (Konventionen, Naming, Guardrails).

## Projektstruktur

```
.
├── data/               # Daten (raw, processed)
├── notebooks/          # Jupyter Notebooks
├── src/                # Source Code
│   └── ds/ # Dein Python Package
├── tests/              # Unit Tests
├── .github/            # CI/CD Workflows
├── .devcontainer/      # Dev Container Config
├── pyproject.toml      # Project & Dependency Config
├── Makefile            # Helper Commands
└── README.md
```

## Notebook-Workflow

- Richtlinien & Naming: siehe `notebooks/README.md`.
- `nbstripout` entfernt Outputs automatisch (pre-commit) – für bestehende Repos `make nbstripout-install` ausführen.
- `nbqa` lintet und fixt Notebooks mit denselben Ruff-Regeln wie für Python-Dateien.
- `make notebooks-run` oder `nox -s notebooks` führen alle Notebooks headless aus.

## Daten-Governance

- Struktur, Guardrails und Naming-Konventionen sind in `data/README.md` dokumentiert.
- `data/raw/` bleibt unverändert und wird weiterhin vom Git-Tracking ausgeschlossen (außer `.gitkeep`).
- `data/processed/` enthält reproduzierbare Artefakte, die jederzeit aus Code regeneriert werden können.
- Hinterlege zu jeder Datenquelle kurz Herkunft, Lizenz und Reproduzierbarkeit.

## Lizenz

MIT

