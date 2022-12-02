---
title: "python -m rich.spinner shows extra lines"
---

The spinner example is know to break on some terminals (Windows in particular).

Some terminals don't display emoji with the correct width, which means Rich can't always align them accurately inside a panel.
