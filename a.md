<!--
Please note that Rich isn't accepting any new features at this point.

If a feature can be implemented without modifying the core library, then
they should be released as a third-party module. I can accept updates to the
core library that make it easier to extend (think hooks).

Bugfixes are always welcome of course.

Sometimes it is not clear what is a feature and what is a bug fix.
If there is any doubt, please open a discussion first.

-->

<!--
*Are you contributing typo fixes?*

If your PR solely consists of typos, at least one must be in the docs to warrant an addition to CONTRIBUTORS.md
-->

## Type of changes

- [x] Bug fix
- [x] New feature
- [ ] Documentation / docstrings
- [x] Tests
- [ ] Other

## AI?

- [ ] AI was used to generate this PR

AI generated PRs may be accepted, but only if @willmcgugan has responded on an issue or discussion.

## Checklist

- [x] I've run the latest [black](https://github.com/psf/black) with default args on new code.
- [x] I've updated CHANGELOG.md and CONTRIBUTORS.md where appropriate (see note about typos above).
- [x] I've added tests for new code.
- [x] I accept that @willmcgugan may be pedantic in the code review.

## Description

Please describe your changes here.

**Important:** Link to an issue or discussion regarding these changes. 

- Added Table.add_row_dict for header-mapped row insertion with auto column creation.
- Added Table.__iadd__ support for single renderables, sequences, and row batches.
- Fixed log output expectations to tolerate line-number and hyperlink variance.
- Guarded markdown and attrs tests with dependency checks to prevent false failures.
- Updated tests to cover the new table additions via existing table test patterns and console capture checks.
