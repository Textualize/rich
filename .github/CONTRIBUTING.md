# Contributing to Rich

This project welcomes contributions in the form of Pull Requests.
For clear bug-fixes / typos etc. just submit a PR.
For new features or if there is any doubt in how to fix a bug, you might want
to open an issue prior to starting work, or email willmcgugan+rich@gmail.com
to discuss it first.

## Prerequisites

Rich uses [poetry](https://python-poetry.org/docs/) for packaging and
dependency management. To start developing with Rich, install Poetry
using the [recommended method](https://python-poetry.org/docs/#installation).

Next, you'll need to create a _fork_ (your own personal copy) of the Rich repository, and clone that fork 
on to your local machine. GitHub offers a great tutorial for this process [here](https://docs.github.com/en/get-started/quickstart/fork-a-repo).
After following this guide, you'll have a local copy of the Rich project installed.

Enter the directory containing your copy of Rich (`cd rich`).

Poetry can be used to create an isolated _virtual environment_ for the project:

```
poetry shell
```

The first time we run `poetry shell`, such an isolated environment is created and forever associated with our project.
Any time we wish to enter this virtual environment again, we simply run `poetry shell` again.

Now we can install the dependencies of Rich into the virtual environment:

```
poetry install
```

The rest of this guide assumes you're inside the virtual environment.
If you're having difficulty running any of the commands that follow,
ensure you're inside the virtual environment by running `poetry shell`.

## Developing

At this point, you're ready to start developing.
Some things to consider while developing Rich code include:

* Ensure new code is documented in docstrings
* Avoid abbreviations in variable or class names
* Aim for consistency in coding style and API design

Before each [commit](https://github.com/git-guides/git-commit), you should:

1. Run the tests and ensure they pass
2. Ensure type-checking passes
3. Format the code using `black`

These steps are described in the following sections.

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

The "Coverage Report" that gets printed to the terminal after the tests run can be used
to identify lines of code that haven't been covered by tests.
If any of the new lines you've added or modified appear in this report, you should strongly consider adding tests which exercise them.

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

Please add type annotations for all new code, and ensure that type checking succeeds before creating a pull request.

### Code Formatting

Rich uses [`black`](https://github.com/psf/black) for code formatting.
I recommend setting up black in your editor to format on save.

To run black from the command line, use `make format-check` to check your formatting,
and use `make format` to format and write to the files.

### Consider Documentation

Consider whether the change you made would benefit from documentation - if the feature has any user impact at all, the answer is almost certainly yes!
Documentation can be found in the `docs` directory.
There are some additional dependencies required to build the documentation. 
These dependencies can be installed by running (from the `docs` directory):

```
pip install -r requirements.txt
```

After updating the documentation, you can build them (from the project root directory) by running:

```
make docs
```

This will generate the static HTML for the documentation site at `docs/build/html`.

### Update CHANGELOG and CONTRIBUTORS

Before submitting your pull request, update the `CHANGELOG.md` file describing, briefly, what you've done.
Be sure to follow the format seen in the rest of the document.

If this is your first time contributing to Rich:

1. Welcome!
2. Be sure to add your name to `CONTRIBUTORS.md`.

### Pre-Commit

We strongly recommend you [install the pre-commit hooks](https://pre-commit.com/#installation) included in the repository.
These automatically run some of the checks described earlier each time you run `git commit`,
and over time can reduce development overhead quite considerably.

## Creating A Pull Request

Once your happy with your change and have ensured that all steps above have been followed (and checks have passed), you can create a pull request.
GitHub offers a guide on how to do this [here](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork).
Please ensure that you include a good description of what your change does in your pull request, and link it to any relevant issues or discussions.

When you create your pull request, we'll run the checks described earlier. If they fail, please attempt to fix them as we're unlikely to be able to review your code until then.
If you've exhausted all options on trying to fix a failing check, feel free to leave a note saying so in the pull request and someone may be able to offer assistance.

### Code Review

After the checks in your pull request pass, someone will review your code.
There may be some discussion and, in most cases, a few iterations will be required to find a solution that works best.

## Afterwards

When the pull request is approved, it will be merged into the `master` branch.
Your change will only be available to users the next time Rich is released. 
