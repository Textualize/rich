test:
	TERM=unknown pytest --cov-report term-missing --cov=rich tests/ -vv
format-check:
	black --check .
format:
	black .
typecheck:
	mypy --no-warn-unused-ignores
typecheck-report:
	mypy -p rich --html-report mypy_report  --no-warn-unused-ignores
.PHONY: docs
docs:
	cd docs; make html
