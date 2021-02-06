---
name: Bug report
about: Create a report to help us improve
title: "[BUG]"
labels: Needs triage
assignees: ""
---

**Read the docs**
You might find a solution to your problem in the [docs](https://rich.readthedocs.io/en/latest/introduction.html) -- consider using the search function there.

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
A minimal code example that reproduces the problem would be a big help if you can provide it. If the issue is visual in nature, consider posting a screenshot.

**Platform**
What platform (Win/Linux/Mac) are you running on? What terminal software are you using?

**Diagnose**
I may ask you to cut and paste the output of the following commands. It may save some time if you do it now.

```
python -m rich.diagnose
python -m rich._windows
pip freeze | grep rich
```
