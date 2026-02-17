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

**Five functions chosen (from lizard Warnings; core library only, excluding third-party/generated):** We chose the **five with the lowest CCN** that still triggered a lizard Warning (CCN > 15 or length > 1000), so that manual cyclomatic complexity count, DIY branch instrumentation, and coverage improvement are easier to verify by hand for this assignment.

| NLOC | CCN | token | PARAM | length | location                                               |
| ---- | --- | ----- | ----- | ------ | ------------------------------------------------------ |
| 80   | 16  | 499   | 3     | 135    | `__rich_console__` @141-275 @ `rich/panel.py` (Panel)  |
| 52   | 17  | 348   | 9     | 55     | `__call__` @32-86 @ `rich/_log_render.py` (Log render) |
| 47   | 17  | 379   | 5     | 57     | `justify` @111-167 @ `rich/containers.py` (Containers) |
| 29   | 17  | 220   | 2     | 59     | `__rich_console__` @156-198 @ `rich/progress_bar.py` (Progress bar) |
| 34   | 17  | 213   | 1     | 37     | `stop` @145-181 @ `rich/live.py` (Live)                |

Lizard columns: NLOC = non-comment lines of code, CCN = cyclomatic complexity number, token = tokens, PARAM = parameter count, length = length in lines.

1. What are your results for five complex functions?
   - Did all methods (tools vs. manual count) get the same result?
   - Are the results clear?
2. Are the functions just complex, or also long?
3. What is the purpose of the functions?
4. Are exceptions taken into account in the given measurements?
5. Is the documentation clear w.r.t. all the possible outcomes?

## Function 1: **rich_console** (Panel)

In @141-275 @ `rich/panel.py`

1. **Did the tool and our manual count match?**
   - The tool (lizard) reports cyclomatic complexity 16 for this function. Cyclomatic complexity is the number of independent paths through the code (each if, else, loop, or condition adds one).
   - Filip counted by hand: every if/elif/else, every ternary (condition ? a : b), and the conditions inside the inner helper `align_text`. Counted 16. So the tool and our manual count give the same result.

2. **Is the function only complex, or also long?** It is both. The function is 80 non-comment lines (135 lines in total in the file). The complexity (16) comes from many branches: for example, whether there is padding or not, how the width is chosen, whether the panel has a title or not, whether it has a subtitle or not, and whether the title/subtitle are left-, center-, or right-aligned. So the code is not extremely long, but it has a lot of decision points.

3. **What does the function do?** This function draws a Panel: a bordered box that can wrap any content (text, tables, etc.) in the terminal. It can show an optional title in the top border and an optional subtitle in the bottom border. It “yields” (produces) the small pieces (segments) that the Rich library then turns into visible output. So its job is to decide what to draw (top border with or without title, content lines with left and right borders, bottom border with or without subtitle) and hand those pieces to the console.

4. **Do we count exceptions (try/except)?** In this function there are no try/except blocks. So when we count branches, we only count if/else and similar. The tool (lizard) and our manual count therefore agree, we did not have to decide how to count exception handlers here.

5. **Is the documentation clear about all the different outcomes?** The inner helper `align_text` has a short docstring that explains its role. The main function does not have a docstring that lists every branch (for example, all three alignment options or when the title or subtitle are present or missing). To understand all possible outcomes, we had to read the code. So the docs help a bit, but they are not enough on their own for someone who wants to see every path the code can take.

## Function 4: **rich_console** (Progress bar)
In @156-198 @ `rich/progress_bar.py`

1. **Did the tool and our manual count match?**
   - Lizard reports cyclomatic complexity 21 for this function. 
   - Jingze manually counted 21: a base complexity of 1, plus contributions from explicit control flow (if) of 9, and boolean/ternary operators of 11. The counts matched.
2. **Is the function only complex, or also long?** 
   
   It is only complex, not long. The function only has about 40 lines of actual executable code. However, it has a high logic density. Almost every line performs a calculation involving a conditional check or an iteration.
3. **What does the function do?** 
   
   This is the core rendering method for the `ProgressBar` widget. It generates the `Segment` objects (text + style) that the console displays.

   It handles determining the width and mode (ASCII/Unicode) and deciding whether to show a "Pulse" animation (for indeterminate progress) or a standard bar; furthermore, it calculates exactly how many "full bars", "half bars", and "empty spaces" are needed based on the completion percentage, while selecting the correct colors and styles for each part (completed, finished, remaining).

4. **Do we count exceptions (try/except)?** 
   
   No. There are no try/except blocks in this function.

5. **Is the documentation clear about all the different outcomes?** 

   The class has a docstring, but this specific method does not. The logic for handling "half bars" and the specific condition for when to draw the "remaining" empty bar (only when color is enabled) is implicit in the code and not explained in documentation.

## Refactoring

Plan for refactoring complex code:

**Function 1 (Panel `__rich_console__`):** Move the inner function `align_text` out.

The inner function `align_text` (left/center/right and the `if excess_space` / `if text.style` branches) can become a private method on the class, e.g. `_align_text(...)`, or a module-level helper. Then `__rich_console__` no longer “contains” those branches for cyclomatic complexity, the main method just calls it.
Estimated impact of refactoring (lower CC, but other drawbacks?): **Lower CC** in the main method. **Possible drawbacks:** one extra method to maintain; behaviour unchanged.

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
