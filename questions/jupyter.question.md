---
title: "Extra space, not enough space, in Jupyter output"
alt_titles:
  - "Extra new line in Jupyter"
  - "Not enough space in Jupyter"
---

There are many different implementations of Jupyter, from different vendors.

Different notebook software may render Rich's output differently, due to how the CSS is constructed.
Adding or removing space, may make the output look good on your software, but break somewhere else.

I have been adding and removing new lines for jupyter since Rich added support, and I am reluctant to continue to do that, *unless* there is some supporting evidence that Rich is doing the wrong thing.
I'm afraid that making it look better for your software isn't evidence.

Without that evidence, I may close issues and PRs for this issue.
I will accept PRs, if sufficient research has been done regarding not breaking other Jupyter implementations (but that is a high bar).

Thanks for undertstanding.
