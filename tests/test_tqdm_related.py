"""Unit-level helpers that mirror tqdm formatting and postfix handling."""

import io

from rich.tqdm import _TqdmWrapper, _TextBackend

# pylint: disable=protected-access


def format_num(n):
    """Intelligent scientific notation (.3g), mirroring tqdm."""

    f = "{0:.3g}".format(n).replace("+0", "+").replace("-0", "-")
    n_str = str(n)
    return f if len(f) < len(n_str) else n_str


def test_format_num_matches_shorter_representation():
    """Ensure numeric formatting mirrors tqdm's shorter-of fixed/scientific rule."""
    assert format_num(1337) == "1337"
    # prefers the shorter of fixed or scientific
    assert format_num(1239876) == "1239876"
    assert format_num(0.00001234) == "1.23e-5"
    assert format_num(-0.1234) == "-.123"


def test_wrapper_accepts_postfix_and_len():
    """Wrapper should expose len() and normalize postfix values."""
    progress = _TqdmWrapper(range(3), total=None)
    assert len(progress) == 3
    progress.update(postfix={"loss": 1.2345})
    assert progress.postfix == {"loss": "1.23"}


def test_set_postfix_allows_multiple_fields():
    """Multiple postfix fields remain formatted to short strings."""
    progress = _TqdmWrapper(range(2), total=2)
    progress.set_postfix({"loss": 0.9876}, acc=0.42)
    assert progress.postfix == {"loss": "0.988", "acc": "0.42"}


def test_set_postfix_str_passthrough():
    """String postfix should pass through unchanged."""
    progress = _TqdmWrapper(range(1), total=1)
    progress.set_postfix_str("done")
    assert progress.postfix == {"postfix": "done"}


def test_wrapper_disable_skips_progress_calls():
    """Disabled wrapper still increments counters without rendering."""
    progress = _TqdmWrapper(range(2), disable=True)
    assert list(progress) == [0, 1]
    # update should not raise when disabled and should still track n
    progress.update(2, postfix={"acc": 0.9})
    assert progress.n == 4


def test_postfix_idempotent_when_unchanged():
    """Calling set_postfix with identical content should keep the same mapping."""
    progress = _TqdmWrapper(range(1), total=1)
    progress.set_postfix({"loss": 1.0})
    first = progress.postfix
    progress.set_postfix({"loss": 1.0})
    assert progress.postfix is first


def test_text_backend_throttles(monkeypatch):
    """Text backend should skip renders inside the mininterval window."""
    backend = _TextBackend(io.StringIO(), mininterval=0.1)
    backend._last_render = -1.0  # noqa: SLF001 ensure first render passes throttle
    ticks = iter([0.0, 0.05, 0.2])
    monkeypatch.setattr("rich.tqdm.time.monotonic", lambda: next(ticks))

    first = backend.render(n=1, total=2, desc="d", postfix={}, leave=True, to_string=False)
    second = backend.render(n=2, total=2, desc="d", postfix={}, leave=True, to_string=False)
    third = backend.render(n=2, total=2, desc="d", postfix={}, leave=True, to_string=False)

    assert first
    assert second == ""  # throttled
    assert third  # rendered after interval


def test_should_render_thresholds():
    """Render should wait for both time and iter thresholds unless postfix changed."""
    progress = _TqdmWrapper(range(1), mininterval=1.0, miniters=2)
    progress._last_render_time = 0.0  # noqa: SLF001
    progress._last_render_n = 0  # noqa: SLF001

    progress.n = 1
    assert progress._should_render(0.5, refresh=False, postfix_changed=False) is False  # noqa: SLF001

    progress.n = 2
    assert progress._should_render(0.5, refresh=False, postfix_changed=False) is False  # noqa: SLF001
    assert progress._should_render(1.0, refresh=False, postfix_changed=False) is True  # noqa: SLF001

    progress._last_render_time = 0.0  # noqa: SLF001
    progress.n = 0
    assert progress._should_render(1.0, refresh=False, postfix_changed=True) is True  # noqa: SLF001


def test_wrapattr_passthrough():
    """wrapattr should forward calls to the underlying method."""
    buf = io.StringIO()
    wrapped = _TqdmWrapper.wrapattr(buf, "write")
    wrapped("ok")
    assert buf.getvalue() == "ok"


def test_external_write_mode_uses_provided_file():
    """external_write_mode should enter with provided file object."""
    buf = io.StringIO()
    cm = _TqdmWrapper.external_write_mode(file=buf)
    with cm as target:
        target.write("line")
    assert buf.getvalue() == "line"


def test_first_update_marks_render(monkeypatch):
    """Initial update should render and record counters instead of throttling away."""
    monkeypatch.setattr("rich.tqdm.time.monotonic", lambda: 100.0)
    progress = _TqdmWrapper(range(1), mininterval=0.1)
    progress.update()

    assert progress._last_render_n == progress.n  # noqa: SLF001


def test_update_after_close_is_noop():
    """Updating after close should be ignored and not bump counters."""
    progress = _TqdmWrapper(range(1))
    progress.close()
    progress.update()

    assert progress.n == 0
