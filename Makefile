test:
	pytest --cov-report term-missing --cov=rich tests/ -v
typecheck:
	mypy -p rich --ignore-missing-imports --warn-unreachable
typecheck-report:
	mypy -p rich --ignore-missing-imports --warn-unreachable --html-report mypy_report
pytype:
	pytype --config=pytype.cfg
.PHONY: docs
docs:
	cd docs; make html
