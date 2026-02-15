# Report for assignment 3

This is a template for your report. You are free to modify it as needed.
It is not required to use markdown for your report either, but the report
has to be delivered in a standard, cross-platform format.

## Project

Name: Rich

URL: https://github.com/DD2480-2026-Group-8/rich-Assignment-3

Rich is a Python library for rich text and beautiful formatting in the terminal (tables, progress bars, markdown, syntax highlighting, and more). We use only the Python code in the `rich/` package.

**Lines of code (Python, assignment requirement ≥10 K LOC):** We used `cloc --include-lang=Python rich` and obtained 31,346 lines of code (100 files), so the project satisfies the size requirement. Output:

```
-------------------------------------------------------------------------------
Language                     files          blank        comment           code
-------------------------------------------------------------------------------
Python                         100           3320           3787          31346
-------------------------------------------------------------------------------
SUM:                           100           3320           3787          31346
-------------------------------------------------------------------------------
```

## Onboarding experience

Did it build and run as documented?

- **Environment:** We use a project virtual environment (`.venv`). All tools (pytest, lizard, coverage) are installed in the venv, not globally. Commands: `source .venv/bin/activate`, then `pip install -e .` (or `poetry install`) for dependencies; `pip install lizard` for complexity measurement.
- **Build:** The project builds and installs without extra steps beyond the README (pip/poetry). No heavy additional tooling was required.
- **Tests:** We run the test suite with `pytest` (config in `pyproject.toml`, test path `tests/`). Result: **936 passed**, 25 skipped, **3 failed**. The three failures are in `test_markdown.py::test_inline_code` and two in `test_syntax.py` (`test_blank_lines`, `test_python_render_simple_indent_guides`). They assert exact ANSI escape sequences (colors/spacing); the actual output differs slightly (e.g. gray vs black for default text, or spacing) due to our Pygments/theme version. These are snapshot-style tests, not functional bugs. We consider the suite usable for coverage and for adding new tests.
- **Complexity measurement:** We ran `lizard rich/ -l python`. Lizard reported 25 functions in its “Warnings” section (high cyclomatic complexity or long length). From these we will choose five functions for manual CC count and coverage work.
- **Plan:** We continue with this project. We have not changed to another one.

**Clarification — environment and docs:** The assignment text does not explicitly require a virtual environment; we used one (`.venv`) to keep tools and versions isolated and reproducible. The project’s main **README.md** is aimed at end users (install with `pip`, run `python -m rich`) and does not describe a developer workflow (venv, running tests, lizard, or coverage).

## Complexity

1. What are your results for five complex functions?
   - Did all methods (tools vs. manual count) get the same result?
   - Are the results clear?
2. Are the functions just complex, or also long?
3. What is the purpose of the functions?
4. Are exceptions taken into account in the given measurements?
5. Is the documentation clear w.r.t. all the possible outcomes?

## Refactoring

Plan for refactoring complex code:

Estimated impact of refactoring (lower CC, but other drawbacks?).

Carried out refactoring (optional, P+):

git diff ...

## Coverage

### Tools

Document your experience in using a "new"/different coverage tool.

How well was the tool documented? Was it possible/easy/difficult to
integrate it with your build environment?

### Your own coverage tool

Show a patch (or link to a branch) that shows the instrumented code to
gather coverage measurements.

The patch is probably too long to be copied here, so please add
the git command that is used to obtain the patch instead:

git diff ...

What kinds of constructs does your tool support, and how accurate is
its output?

### Evaluation

1. How detailed is your coverage measurement?

2. What are the limitations of your own tool?

3. Are the results of your tool consistent with existing coverage tools?

## Coverage improvement

Show the comments that describe the requirements for the coverage.

Report of old coverage: [link]

Report of new coverage: [link]

Test cases added:

git diff ...

Number of test cases added: two per team member (P) or at least four (P+).

## Self-assessment: Way of working

Current state according to the Essence standard: ...

Was the self-assessment unanimous? Any doubts about certain items?

How have you improved so far?

Where is potential for improvement?

## Overall experience

What are your main take-aways from this project? What did you learn?

Is there something special you want to mention here?
