# Benchmarking Rich

This directory contains benchmarks, for monitoring the performance of Rich over time.

The benchmarks use a tool called [Airspeed Velocity](https://asv.readthedocs.io/en/stable) (`asv`),
and we've configured it in [asv.conf.json](../asv.conf.json).

## Running Benchmarks

We strongly recommend running `asv run --help` for a full list of options, but
here are some common actions:

* You can run the benchmarks against the `master` branch with `asv run`.
* To test the most recent commit on your branch `asv run HEAD^!`.
* To generate a static website for browsing the results, run `asv publish`. The resulting HTML can be found in `benchmarks/html`.

The asv docs have some more examples [here](https://asv.readthedocs.io/en/stable/using.html#benchmarking).
