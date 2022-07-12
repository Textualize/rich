# Benchmarking Rich

This directory contains benchmarks, for monitoring the performance of Rich over time.

View the benchmark dashboard [here](https://textualize.github.io/rich-benchmarks/).

The benchmarks use a tool called [Airspeed Velocity](https://asv.readthedocs.io/en/stable) (`asv`),
and we've configured it in [asv.conf.json](../asv.conf.json).

## Running Benchmarks

We strongly recommend running `asv run --help` for a full list of options, but
here are some common actions:

* You can run the benchmarks against the `master` branch with `asv run`.
* To test the most recent commit on your branch `asv run HEAD^!`.
* To generate a static website for browsing the results, run `asv publish`. The resulting HTML can be found in `benchmarks/html`.

The asv docs have some more examples [here](https://asv.readthedocs.io/en/stable/using.html#benchmarking).

## Updating the Benchmark Website

1. Ensure any tags you wish to benchmark are included in the file `asvhashfile` at the root of the repo.
2. Run the benchmarks for those tags by running `asv run HASHFILE:asvhashfile`. This will take several minutes.
3. Create the HTML locally for those benchmarks by running `asv publish`.
4. Run `asv preview` to launch a local webserver that will let you preview the benchmarks dashboard. Navigate to the URL this command gives you and check everything looks fine.
5. Checkout the `rich-benchmarks` repo from [here](https://github.com/Textualize/rich-benchmarks) and `cd` into it.
6. Copy the HTML you generated earlier into the root of this repo, e.g. `cp -r ../rich/benchmarks/html/* .` (assuming you checked out `rich-benchmarks` alongside `rich` in your filesystem)
7. When the HTML is merged into `main`, the [benchmark dashboard](https://textualize.github.io/rich-benchmarks/) will be updated automatically via a GitHub Action.
