---
name: Bug report
about: Create a report to help us improve
title: "[BUG]"
labels: Needs triage
assignees: ""
---

You may find a solution to your problem in the [docs](https://rich.readthedocs.io/en/latest/introduction.html) or [issues](https://github.com/textualize/rich/issues).

**Describe the bug**

Edit this with a clear and concise description of what the bug.

Provide a minimal code example that demonstrates the issue if you can. If the issue is visual in nature, consider posting a screenshot.

**Platform**
<details>
<summary>Click to expand</summary>

What platform (Win/Linux/Mac) are you running on? What terminal software are you using?

I may ask you to copy and paste the output of the following commands. It may save some time if you do it now.

If you're using Rich in a terminal:

```
python -m rich.diagnose
pip freeze | grep rich
```

If you're using Rich in a Jupyter Notebook, run the following snippet in a cell
and paste the output in your bug report.

```python
from rich.diagnose import report
report()
```

</details>
