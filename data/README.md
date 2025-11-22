# Data Layout

This repository follows a lightweight version of the Cookiecutter-Data-Science convention:

- `raw/` – immutable source files as delivered by stakeholders or public APIs.
- `processed/` – intermediate artifacts that are reproducible from `raw/` via notebooks or scripts.

## Guardrails

1. **Never commit sensitive or large raw data.** Keep `.gitignore` in place and push only metadata-free placeholders (`.gitkeep`, README files, schemas, etc.).
2. **Document provenance.** Drop a short Markdown file next to every dataset summarizing where it came from and how to reproduce it.
3. **Make processing reproducible.** Prefer storing code (not binary artifacts) in `src/` or `notebooks/` that knows how to regenerate anything inside `processed/`.
4. **Use deterministic file names.** Encode date ranges or parameter names in filenames so it is obvious how outputs relate to the inputs.
5. **Cache responsibly.** If derived datasets are truly huge, keep them locally (or in object storage) and reference them via environment variables or `.env` files instead of committing them.

## Suggested workflow

1. Land new raw data under `data/raw/<source>/<yyyymmdd>/...` and immediately add a short README with context.
2. Reference raw files from notebooks or ETL scripts using `pathlib.Path("data/raw/...")` so relative paths continue to work inside dev containers and CI.
3. Write results back under `data/processed/` with clear suffixes such as `_features.parquet`, `_model.pkl`, etc.
4. When automations (e.g., `make notebooks-run` or `nox -s notebooks`) execute, they should regenerate everything under `data/processed/` from scratch.
