---
title: "Why does emoji break alignment in a Table or Panel?"
---

Rich uses python wcwidth for character width measurement, which follows a [specification](https://wcwidth.readthedocs.io/en/latest/specs.html) that includes support for complex emoji and languages (grapheme clustering).

Although *all* terminals do not fully support complex emoji, Rich support matches the correct presentation of many actively developed terminal emulators, tabulated and reported as [ucs-detect results](https://ucs-detect.readthedocs.io/results.html).
