build:
	python3 -m pip install --upgrade pip
	pip install wheel
	pip install poetry
	pip install -r requirements/requirements.txt
	pip install -r requirements/test_requirements.txt
	pip install -r requirements/typecheck_requirements.txt
	pip install -r requirements/docs_requirements.txt
	poetry install
	pip install .
test:
	pytest --cov=rich --cov-report xml:cov.xml -vv tests/
typecheck:
	mypy -p rich --ignore-missing-imports --warn-unreachable
typecheck-report:
	mypy -p rich --ignore-missing-imports --warn-unreachable --html-report mypy_report
pytype:
	pytype --config=pytype.cfg
.PHONY: docs
docs:
	cd docs; make html
