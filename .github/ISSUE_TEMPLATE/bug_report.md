---
name: Bug report
about: Create a report to help us improve
title: "[BUG]"
labels: Needs triage
assignees: ""
---

- [ ] I've checked [docs](https://rich.readthedocs.io/en/latest/introduction.html) and [closed issues](https://github.com/Textualize/rich/issues?q=is%3Aissue+is%3Aclosed) for possible solutions.
- [ ] I can't find my issue in the [FAQ](https://github.com/Textualize/rich/blob/master/FAQ.md).

<!-- 
WAIT! Is this a feature request?

Rich isn't accepting new features. If it can be implemented in a third-party library, then that is what I recommend.

Rich *may* accept enhancements to existing features, if they don't have a disruptive impact on the API.

If you think your feature is exceptional, then please make your case in a discussion.
-->

**Describe the bug**

Edit this with a clear and concise description of what the bug.

Provide a minimal code example that demonstrates the issue if you can.
Please ensure that your example runs without modification (don't forget imports).

If the issue is visual in nature, consider posting a screenshot.

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
