# Contributing to Rich

This project welcomes contributions in the form of Pull Requests.
For clear bug-fixes / typos etc. just submit a PR.
For new features or if there is any doubt in how to fix a bug, you might want
to open an issue prior to starting work, or email willmcgugan+rich@gmail.com
to discuss it first.

## Development Environment

Rich uses [poetry](https://python-poetry.org/docs/) for packaging and
dependency management. To start developing with Rich, install Poetry
using the [recommended method](https://python-poetry.org/docs/#installation) or run:

```
pip install poetry
```

Once Poetry is installed, install the dependencies with the following command:

```
poetry install
```

### Tests

Run tests with the following command:

```
make test
```

Or if you don't have `make`, run the following:

```
pytest --cov-report term-missing --cov=rich tests/ -vv
```

New code should ideally have tests and not break existing tests.

### Type Checking

Rich uses type annotations throughout, and `mypy` to do the checking.
Run the following to type check Rich:

```
make typecheck
```

Or if you don't have `make`:

```
mypy -p rich --config-file= --ignore-missing-imports --no-implicit-optional --warn-unreachable
```

Please add type annotations for all new code.

### Code Formatting

Rich uses [`black`](https://github.com/psf/black) for code formatting.
I recommend setting up black in your editor to format on save.

To run black from the command line, use `make format-check` to check your formatting,
and use `make format` to format and write to the files.
