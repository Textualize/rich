test:
	TERM=unknown uv run pytest --cov-report term-missing --cov=rich tests/ -vv
test-no-cov:
	TERM=unknown uv run pytest tests/ -vv
format-check:
	uv run black --check .
format:
	uv run black .
typecheck:
	uv run mypy -p rich --no-incremental
typecheck-report:
	uv run mypy -p rich --html-report mypy_report
.PHONY: docs
docs:
	uv run --group docs sphinx-build -M html docs/source docs/build
