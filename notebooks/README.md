# Notebook Conventions

1. **Keep outputs light.** Pre-commit runs `nbstripout` so JSON payloads stay small. Treat notebooks as source files; regenerate plots on demand.
2. **Name with intent.** Prefix with an ordinal (`01_`, `02_`) to preserve execution order and suffix with the main question, e.g., `02_feature_engineering.ipynb`.
3. **Reference data via relative paths.** Use `Path("data/raw/...")` and keep secrets (API tokens, database URLs) in `.env` files loaded via `python-dotenv` or VS Code secrets.
4. **Promote shared logic.** Once code stabilizes, move it into `src/ds/` so tests can cover it and notebooks stay concise.
5. **Automate execution.** `make notebooks-run` executes all notebooks headlessly; keep runtime manageable (<5 min) so CI or reviewers can reproduce results.

## Handy commands

```bash
make notebook       # launch Jupyter Lab rooted at ./notebooks
make nbqa           # lint notebooks with nbqa + Ruff
make notebooks-run  # execute every *.ipynb headlessly via nbconvert
make nbstripout-install  # install git filter to strip outputs on commit
```
