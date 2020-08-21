# Contributing to Rich

This project welcomes contributions in the form of Pull Requests. For clear bug-fixes / typos etc. just submit a PR. For new features or if there is any doubt in how to fix a bug, you might want to open an issue prior to starting work, or email willmcgugan+rich@gmail.com to discuss it first.

## Development Environment

To start developing with Rich, first create a _virtual environment_ then run the following to install development requirements:

```
pip install -r requirements-dev.txt
poetry install
```

### Tests

Run tests with the following command:

```
make test
```

Or if you don't have make, run the following:

```
pytest --cov-report term-missing --cov=rich tests/ -vv
```

New code should ideally have tests and not break existing tests.

### Type Checking

Rich uses type annotations throughout, and `mypy` to do the checking. Run the following to type check Rich:

```
make typecheck
```

Or if you don't have `make`:

```
mypy -p rich --ignore-missing-imports --warn-unreachable
```

Please add type annotations for all new code.

### Code Formatting

Rich uses [`black`](https://github.com/psf/black) for code formatting.
I recommend setting up black in your editor to format on save.

To run black from the command line, use `make format-check` to check your formatting,
and use `make format` to format and write to the files.