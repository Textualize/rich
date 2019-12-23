test:
	pytest --cov-report term-missing --cov=rich tests/ -v
typecheck:
	mypy -p rich --python-version 3.7 --ignore-missing-imports --warn-unreachable
typecheck-report:
	mypy -p rich --python-version 3.7 --ignore-missing-imports --warn-unreachable --html-report mypy_report
