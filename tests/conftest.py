import pytest


@pytest.fixture(autouse=True)
def reset_color_envvars(monkeypatch):
    """Remove color-related envvars to fix test output"""
    monkeypatch.delenv("FORCE_COLOR", raising=False)
    monkeypatch.delenv("NO_COLOR", raising=False)
