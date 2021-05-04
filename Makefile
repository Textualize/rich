test:
	pytest --cov-report term-missing --cov=rich tests/ -vv
format-check:
	black --check .
format:
	black .
typecheck:
	mypy -p rich --config-file= --ignore-missing-imports --no-implicit-optional --warn-unreachable
typecheck-report:
	mypy -p rich --config-file= --ignore-missing-imports --no-implicit-optional --warn-unreachable --html-report mypy_report
.PHONY: docs
docs:
	cd docs; make html
