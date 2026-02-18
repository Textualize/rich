def pytest_sessionfinish(session, exitstatus):
    from rich._log_render import BRANCH_COVERAGE

    print("\nBRANCH COVERAGE DIY ")
    for i in sorted(BRANCH_COVERAGE):
        print(f"{i}: {BRANCH_COVERAGE[i]}")