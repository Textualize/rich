def pytest_sessionfinish(session, exitstatus):
    # Adjust import to the module that contains BRANCH_COVERAGE
    from rich._log_render import BRANCH_COVERAGE

    print("\n=== DIY BRANCH COVERAGE ===")
    for bid in sorted(BRANCH_COVERAGE):
        print(f"{bid}: {BRANCH_COVERAGE[bid]}")