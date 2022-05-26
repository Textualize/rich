TEST_KW?=
VERBOSE?=1
COVERAGE?=1

test:
	TERM=unknown pytest \
	$(if $(findstring 1,$(COVERAGE)),--cov-report term-missing --cov=rich) \
	$(if $(findstring 1,$(VERBOSE)),-vv) \
	-k $(TEST_KW) \
	tests/
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
