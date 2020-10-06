test:
	pytest --cov-report term-missing --cov=rich tests/ -vv
lint:
	pre-commit run -a
format:
	pre-commit run black -a
typecheck:
	pre-commit run mypy -a
typecheck-report:
	mypy -p rich --ignore-missing-imports --warn-unreachable --html-report mypy_report
.PHONY: docs
docs:
	cd docs; make html
