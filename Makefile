.PHONY: install test lint format nbqa notebook notebooks-run nbstripout-install qa clean

install:
	uv sync --all-extras --dev

test:
	uv run pytest

lint:
	uv run ruff check .

format:
	uv run ruff format .

nbqa:
	@if ls notebooks/*.ipynb >/dev/null 2>&1; then \
		uv run nbqa ruff --fix notebooks; \
	else \
		echo "nbqa: no notebooks found (skipping)"; \
	fi

notebook:
	uv run jupyter lab --notebook-dir notebooks

notebooks-run:
	uv run python scripts/execute_notebooks.py

nbstripout-install:
	uv run nbstripout --install --attributes .gitattributes

qa:
	uv run nox -s qa

clean:
	rm -rf .venv
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
