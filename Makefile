test:
	TERM=unknown pytest --cov-report term-missing --cov=rich tests/ -vv
format-check:
	black --check .
format:
	black .
typecheck:
	mypy -p rich --no-incremental
typecheck-report:
	mypy -p rich --html-report mypy_report
.PHONY: docs
docs:
	cd docs; make html
