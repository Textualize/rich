"""Compatibility shim to replace ``tqdm`` with Rich's progress bars.

Rationale
---------
- Opt-in bridge: call :func:`install_tqdm` to monkeypatch ``tqdm`` symbols
    (``tqdm``, ``trange``, notebook variants) in imported modules **and** any
    already-imported aliases found in ``sys.modules``. The shim stays inert until
    you install it; uninstall with :func:`uninstall_tqdm`.
- Keep call sites stable: the wrapper preserves the common tqdm surface area
    (iteration, len(), postfix, write, wrapattr) while routing rendering through
    :class:`rich.progress.Progress`.
- Favor performance: reuses a shared global ``Progress`` when no custom console
    or file is supplied, throttles refreshes via ``mininterval``/``miniters`` and
    optional ``maxinterval``, and caches formatted postfix values to avoid string
    churn when metrics are unchanged.
- Handle non-interactive outputs: a simplified text backend is used when
    ``partial=True`` with a file-like target to approximate tqdm's plain output
    without Rich's live rendering.

This shim aims to be compatible with the most common tqdm usage patterns, but
it does not implement every tqdm argument. Unrecognized kwargs are ignored
rather than raising, matching tqdm's permissive behavior.
"""

# pylint: disable=missing-function-docstring, import-outside-toplevel

from __future__ import annotations

import importlib
import sys
import time
import types
import threading
from types import TracebackType
from typing import (
    Any,
    Callable,
    ContextManager,
    Dict,
    IO,
    Iterable,
    Iterator,
    List,
    Optional,
    Tuple,
    Type,
    cast,
    Reversible,
    Literal,
)


_PATCH_STATE: Dict[str, Any] = {
    "installed": False,
    "patched_modules": [],  # list of (module, attr, original)
    "replaced_locations": [],  # list of (module, name, original)
}

_GLOBAL_STATE: Dict[str, Optional[Any]] = {"progress": None}


class _DummyLock:
    def __enter__(self) -> _DummyLock:
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> Literal[False]:
        return False


def _format_interval(seconds: float) -> str:
    # Simplified copy of tqdm.format_interval
    minutes, sec = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours:d}:{minutes:02d}:{sec:02d}"
    return f"{minutes:02d}:{sec:02d}"


def _format_postfix_value(value: Any) -> Any:
    if isinstance(value, (int, float)):
        formatted = f"{value:.3g}"
        value_str = str(value)
        return formatted if len(formatted) < len(value_str) else value_str
    return value if isinstance(value, str) else str(value)


def format_num(n: Any) -> str:
    formatted = str(_format_postfix_value(n))
    return formatted.replace("e+0", "e+").replace("e-0", "e-")


def format_interval(t: float) -> str:
    return _format_interval(t)


def format_meter(
    n: float, total: Optional[float], elapsed: float, prefix: str = "", **_: Any
) -> str:
    total_str = "?" if total is None else format_num(total)
    percentage: float
    if total is None or total == 0:
        percentage = 0.0
    else:
        percentage = 100 * n / total
    elapsed_str = _format_interval(elapsed)
    rate = n / elapsed if elapsed > 0 else 0
    rate_str = "?" if rate == 0 else format_num(rate)
    return (
        f"{prefix}{percentage:3.0f}%|          | {format_num(n)}/{total_str} "
        f"[{elapsed_str}<?, {rate_str}it/s]"
    )


def _get_progress(console: Any = None, file: Any = None) -> Tuple[Any, bool]:
    """Return a Progress instance and whether it is shared/global."""

    if console is not None or file is not None:
        from .progress import Progress
        from .console import Console

        prog_console = console or Console(file=file)
        progress = Progress(console=prog_console)
        progress.start()
        return progress, False

    progress = cast("Progress", _GLOBAL_STATE["progress"])
    if progress is None:
        from . import get_console
        from .progress import Progress

        progress = Progress(console=get_console())
        progress.start()
        _GLOBAL_STATE["progress"] = progress
    return progress, True


def _stop_global_progress() -> None:
    progress = _GLOBAL_STATE.get("progress")
    if progress is not None:
        try:
            progress.stop()
        finally:
            _GLOBAL_STATE["progress"] = None


def _attach_api_shims(obj: Any) -> None:
    """Attach tqdm-compatible helper functions and class variables to a callable."""
    # pylint: disable=protected-access
    obj.format_num = format_num
    obj.format_interval = format_interval
    obj.format_meter = format_meter
    obj.write = _TqdmWrapper.write
    obj.get_lock = _TqdmWrapper.get_lock
    obj.set_lock = _TqdmWrapper.set_lock
    obj.external_write_mode = _TqdmWrapper.external_write_mode
    obj.wrapattr = _TqdmWrapper.wrapattr
    obj._instances = _TqdmWrapper._instances
    obj._lock = None


class _TextBackend:
    """Minimal text renderer for partial compatibility mode."""

    def __init__(self, stream: IO[str], mininterval: float) -> None:
        self.stream = stream
        self.mininterval = mininterval
        self._last_render = 0.0

    def render(
        self,
        *,
        n: int,
        total: Optional[int],
        desc: str,
        postfix: Dict[Any, Any],
        leave: bool,
        to_string: bool,
    ) -> str:
        now = time.monotonic()
        if not to_string and now - self._last_render < self.mininterval:
            return ""
        self._last_render = now

        percent = 0 if not total else (n / total * 100 if total else 0)
        bar_len = 10
        done = int(bar_len * (0 if not total else min(1.0, n / float(total))))
        abar = "#" * done + " " * (bar_len - done)
        total_str = "?" if total is None else str(total)
        line = f"\r{percent:3.0f}%|{abar}| {n}/{total_str} [00:00<]"
        if desc:
            line = f"{desc} {line}"
        if postfix:
            postfix_str = ", ".join(f"{k}={v}" for k, v in postfix.items())
            line = f"{line} {postfix_str}"
        if to_string:
            return line.strip()
        if not leave and total is not None and n >= total:
            return line
        try:
            self.stream.write(line)
        except (OSError, ValueError):
            return line
        return line


class _TqdmWrapper:
    """Lightweight stand-in for ``tqdm`` based on Rich progress with render throttling."""

    _instances: List[Any] = []
    _lock_obj: Any = None

    def __init__(
        self,
        iterable: Optional[Iterable[Any]] = None,
        total: Optional[int] = None,
        desc: Optional[str] = None,
        leave: bool = True,
        disable: bool = False,
        initial: int = 0,
        console: Any = None,
        file: Any = None,
        partial: bool = False,
        mininterval: float = 0.1,
        maxinterval: Optional[float] = None,
        miniters: Optional[int] = None,
        ascii: bool = False,  # pylint: disable=redefined-builtin
        smoothing: Optional[float] = None,
        unit: str = "it",
        unit_scale: bool = False,
        unit_divisor: int = 1000,
        bar_format: Optional[str] = None,
        **_: Any,
    ) -> None:
        del smoothing, unit, unit_scale, unit_divisor, bar_format
        self._iterable = iterable
        self._total = total if total is not None else None
        self._desc = desc or ""
        self._leave = leave
        self.desc = self._desc
        self._closed = False
        self._disabled = disable
        self._progress: Optional[Any] = None
        self._task: Optional[Any] = None
        self._write_stream: Optional[IO[str]] = None
        self._partial = partial
        self._use_text_backend = bool(partial and file is not None)
        self._text_backend: Optional[_TextBackend] = None
        self.dynamic_miniters = True
        self.ascii = ascii
        self._lock: Optional[Any] = None
        self.postfix: Optional[Dict[Any, Any]] = {0: {}}
        self.n = initial
        self._is_global = False
        self._mininterval = mininterval
        self._maxinterval = maxinterval
        self._miniters = 1 if miniters is None else max(1, int(miniters))
        # Seed render markers so the first update is eligible to render promptly.
        self._last_render_time = 0.0
        self._last_render_n = self.n

        if self._total is None and hasattr(iterable, "__len__"):
            try:
                self._total = len(iterable)  # type: ignore[arg-type]
            except (TypeError, OverflowError):
                self._total = None

        if self._use_text_backend:
            self._write_stream = file
            self._text_backend = _TextBackend(file, mininterval)
        if not self._disabled and not self._use_text_backend:
            self._progress, self._is_global = _get_progress(console=console, file=file)
            if self._progress is not None:
                self._task = self._progress.add_task(self._desc, total=self._total)
                if initial:
                    self._progress.update(self._task, completed=initial)

    def __iter__(self) -> Iterator[Any]:
        """Iterate while tracking progress updates, honoring disabled/text modes."""
        if self._iterable is None:
            return iter(())
        iterator = iter(self._iterable)
        if self._disabled:
            return self._iter_disabled(iterator)
        if self._use_text_backend:
            self._maybe_render_text()
        return self._iter_enabled(iterator)

    def _iter_disabled(self, iterator: Iterator[Any]) -> Iterator[Any]:
        """Yield items while disabled, tracking count without rendering."""
        for item in iterator:
            self.n += 1
            yield item

    def _iter_enabled(self, iterator: Iterator[Any]) -> Iterator[Any]:
        """Yield items, updating progress each step and closing if not leaving."""
        for item in iterator:
            yield item
            self.update(1)
        if not self._leave:
            self.close()

    def update(
        self,
        n: int = 1,
        *,
        postfix: Optional[Dict[str, Any]] = None,
        refresh: bool = False,
    ) -> None:
        """Advance the bar and conditionally refresh based on throttling thresholds."""
        if self._closed:
            return
        self.n += n
        postfix_changed = False
        if postfix:
            new_postfix = {k: _format_postfix_value(v) for k, v in postfix.items()}
            if new_postfix != (self.postfix or {}):
                self.postfix = new_postfix
                postfix_changed = True
        if self._disabled:
            return
        if self._use_text_backend:
            self._maybe_render_text()
            return
        progress = self._progress
        task = self._task
        if progress is None or task is None:
            return
        now = time.monotonic()
        should_refresh = self._should_render(
            now, refresh=refresh, postfix_changed=postfix_changed
        )
        progress.update(task, advance=n, postfix=self.postfix, refresh=should_refresh)
        if should_refresh:
            self._mark_render(now)

    def set_description(self, desc: str = "") -> None:
        if self._closed:
            return
        self._desc = str(desc)
        if self._disabled:
            return
        self.desc = self._desc
        if self._use_text_backend:
            self._maybe_render_text()
            return
        progress = self._progress
        task = self._task
        if progress is None or task is None:
            return
        now = time.monotonic()
        progress.update(task, description=self._desc, refresh=True)
        self._mark_render(now)

    def set_postfix(
        self,
        ordered_dict: Optional[Dict[str, Any]] = None,
        refresh: bool = True,
        **kwargs: Any,
    ) -> None:
        """Update postfix fields while reusing the last render unless content changed."""
        if self._closed:
            return
        combined: Dict[str, Any] = {}
        if ordered_dict:
            combined.update(ordered_dict)
        if kwargs:
            combined.update(kwargs)
        postfix_changed = False
        if combined:
            new_postfix = {k: _format_postfix_value(v) for k, v in combined.items()}
            if new_postfix != (self.postfix or {}):
                self.postfix = new_postfix
                postfix_changed = True
        if self._disabled:
            return
        if self._use_text_backend:
            self._maybe_render_text()
            return
        progress = self._progress
        task = self._task
        if progress is None or task is None:
            return
        now = time.monotonic()
        should_refresh = self._should_render(
            now, refresh=refresh, postfix_changed=postfix_changed
        )
        progress.update(task, postfix=self.postfix, refresh=should_refresh)
        if should_refresh:
            self._mark_render(now)

    def set_postfix_str(self, s: str = "", refresh: bool = True) -> None:
        self.set_postfix({"postfix": s}, refresh=refresh)

    def close(self) -> None:
        if self._closed:
            return
        if not self._disabled and self._progress and self._task is not None:
            self._progress.remove_task(self._task)
        self._closed = True
        try:
            self._instances.remove(self)
        except ValueError:
            pass
        if self._progress and not self._progress.tasks and self._is_global:
            _stop_global_progress()

    def refresh(self) -> None:
        if self._disabled:
            return
        if self._closed:
            return
        if self._use_text_backend:
            self._maybe_render_text()
            return
        if self._progress is None:
            return
        self._progress.refresh()

    def __len__(self) -> int:
        if self._total is not None:
            return int(self._total)
        if self._iterable is not None:
            try:
                return len(self._iterable)  # type: ignore[arg-type]
            except TypeError:
                pass
        raise TypeError("object of type '_TqdmWrapper' has no len()")

    def __bool__(self) -> bool:
        return bool(self._total or self._iterable)

    def __repr__(self) -> str:
        return self._maybe_render_text(to_string=True)

    def __lt__(self, other: Any) -> bool:
        try:
            return (self._total or 0) < (getattr(other, "_total", 0) or 0)
        except (AttributeError, TypeError):
            return False

    def __enter__(self) -> _TqdmWrapper:
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self.close()

    def __contains__(self, item: Any) -> bool:
        if self._iterable is None:
            return False
        try:
            return item in self._iterable
        except (TypeError, ValueError):
            return False

    def __reversed__(self) -> Iterator[Any]:
        if self._iterable is None:
            raise TypeError("_TqdmWrapper object is not reversible")
        try:
            reversible = cast(Reversible[Any], self._iterable)
            return reversed(reversible)
        except (TypeError, AttributeError) as exc:
            raise TypeError("_TqdmWrapper object is not reversible") from exc

    def _maybe_render_text(self, to_string: bool = False) -> str:
        if not self._text_backend:
            return ""
        postfix_items = {k: v for k, v in (self.postfix or {}).items() if k != 0 and v}
        return self._text_backend.render(
            n=self.n,
            total=self._total,
            desc=self._desc,
            postfix=postfix_items,
            leave=self._leave,
            to_string=to_string,
        )

    def _should_render(
        self, now: float, *, refresh: bool, postfix_changed: bool = False
    ) -> bool:
        """Decide whether to render based on min interval/iters and optional max interval."""
        if refresh:
            return True
        delta_time = now - self._last_render_time
        delta_n = self.n - self._last_render_n
        if postfix_changed and delta_time >= self._mininterval:
            return True
        if delta_time >= self._mininterval and delta_n >= self._miniters:
            return True
        if self._maxinterval is not None and delta_time >= self._maxinterval:
            return True
        return False

    def _mark_render(self, now: float) -> None:
        """Record the last render time and counter for subsequent throttling decisions."""
        self._last_render_time = now
        self._last_render_n = self.n

    def set_description_str(self, desc: str = "") -> None:
        self.set_description(desc)

    def reset(self, total: Optional[int] = None) -> None:
        if total is not None:
            self._total = total
        self.n = 0
        if self._use_text_backend:
            self._maybe_render_text()
        elif self._progress and self._task is not None:
            self._progress.reset(self._task, total=self._total)

    def unpause(self) -> None:
        return

    def clear(self, nolock: bool = False) -> None:
        del nolock
        if self._use_text_backend and self._write_stream is not None:
            try:
                self._write_stream.write("\n")
            except (OSError, ValueError):
                return
        return

    @classmethod
    def write(
        cls,
        s: str,
        file: Optional[IO[str]] = None,
        end: str = "\n",
        nolock: bool = False,
    ) -> None:
        del nolock
        target = file or sys.stderr
        try:
            target.write(str(s) + end)
        except (OSError, ValueError):
            return

    @classmethod
    def get_lock(cls) -> Any:
        if cls._lock_obj is None:
            try:
                cls._lock_obj = threading.Lock()
            except (OSError, RuntimeError):
                cls._lock_obj = _DummyLock()
        return cls._lock_obj

    @classmethod
    def set_lock(cls, lock: Any) -> None:
        cls._lock_obj = lock

    @classmethod
    def external_write_mode(
        cls, file: Optional[IO[str]] = None, nolock: bool = False
    ) -> ContextManager[IO[str]]:
        """Context manager mirroring tqdm.external_write_mode for compatibility."""

        del nolock

        class _CM:
            def __enter__(self) -> IO[str]:
                return file or sys.stderr

            def __exit__(
                self,
                exc_type: Optional[Type[BaseException]],
                exc: Optional[BaseException],
                tb: Optional[TracebackType],
            ) -> Literal[False]:
                return False

        return _CM()

    @classmethod
    def wrapattr(
        cls,
        stream: Any,
        method: str,
        total: Optional[int] = None,
        bytes: bool = False,  # pylint: disable=redefined-builtin
        **kwargs: Any,
    ) -> Any:
        """Wrap a stream attribute call for compatibility with tqdm's wrapattr."""
        del total, bytes, kwargs
        func = getattr(stream, method)

        class _Wrap:
            def __init__(self, fn: Callable[..., Any]):
                self._fn = fn

            def __call__(self, *a: Any, **k: Any) -> Any:
                return self._fn(*a, **k)

            def __getattr__(self, name: str) -> Any:
                return getattr(self._fn, name)

            def __enter__(self) -> "_Wrap":
                return self

            def __exit__(
                self,
                exc_type: Optional[Type[BaseException]],
                exc: Optional[BaseException],
                tb: Optional[TracebackType],
            ) -> Literal[False]:
                return False

            def write(self, data: Any) -> Any:
                return self._fn(data)

        return _Wrap(func)

    def __del__(self) -> None:
        if getattr(self, "_closed", True):
            return
        self.close()


def _make_tqdm_callable(
    console: Any = None, *, partial: bool = False
) -> Callable[[Optional[Iterable[Any]]], _TqdmWrapper]:
    def _tqdm(iterable: Optional[Iterable[Any]] = None, **kwargs: Any) -> _TqdmWrapper:
        return _TqdmWrapper(
            iterable=iterable, console=console, partial=partial, **kwargs
        )

    _attach_api_shims(_tqdm)

    return _tqdm


def _make_trange(
    console: Any = None, *, partial: bool = False
) -> Callable[..., _TqdmWrapper]:
    def _trange(*args: Any, **kwargs: Any) -> _TqdmWrapper:
        return _make_tqdm_callable(console, partial=partial)(range(*args), **kwargs)

    _attach_api_shims(_trange)

    return _trange


def install_tqdm(console: Any = None, *, partial: bool = False) -> None:
    """Monkeypatch ``tqdm`` symbols to use Rich progress.

    Args:
        console: Optional Console to route progress output through.
        partial: When True, enable simplified text rendering for file-like outputs to
            approximate tqdm aesthetics. When False (default), favor the Rich progress
            presentation and avoid extra tqdm-style formatting.
    """

    if _PATCH_STATE["installed"]:
        return

    module_names = ["tqdm", "tqdm.std", "tqdm.auto", "tqdm.notebook"]
    target_attrs = ["tqdm", "trange", "tqdm_notebook", "tnrange"]

    replacements: Dict[Any, Any] = {}
    to_patch: List[Tuple[types.ModuleType, str, Any]] = []

    for modname in module_names:
        try:
            mod = importlib.import_module(modname)
        except ImportError:
            continue
        for attr in target_attrs:
            if not hasattr(mod, attr):
                continue
            orig = getattr(mod, attr)
            if orig in replacements:
                continue
            newobj = (
                _make_tqdm_callable(console, partial=partial)
                if attr in ("tqdm", "tqdm_notebook")
                else _make_trange(console, partial=partial)
            )
            replacements[orig] = newobj
            to_patch.append((mod, attr, orig))

    replaced_locations: List[Tuple[types.ModuleType, str, Any]] = []
    for orig, newval in list(replacements.items()):
        for module in list(sys.modules.values()):
            moddict = getattr(module, "__dict__", None)
            if not isinstance(moddict, dict):
                continue
            for name, val in list(moddict.items()):
                if val is orig:
                    replaced_locations.append((module, name, orig))
                    try:
                        setattr(module, name, newval)
                    except (AttributeError, TypeError):
                        continue

    patched_modules: List[Tuple[types.ModuleType, str, Any]] = []
    for mod, attr, orig in to_patch:
        replacement: Any = replacements.get(orig)
        if replacement is None:
            continue
        new_callable = cast(Callable[..., Any], replacement)
        try:
            setattr(mod, attr, new_callable)
            patched_modules.append((mod, attr, orig))
        except (AttributeError, TypeError):
            continue

    _PATCH_STATE["installed"] = True
    _PATCH_STATE["patched_modules"] = patched_modules
    _PATCH_STATE["replaced_locations"] = replaced_locations


def uninstall_tqdm() -> None:
    """Revert monkeypatching performed by :func:`install_tqdm`."""

    if not _PATCH_STATE["installed"]:
        return

    for module, name, orig in _PATCH_STATE.get("replaced_locations", []):
        try:
            setattr(module, name, orig)
        except (AttributeError, TypeError):
            continue

    for module, attr, orig in _PATCH_STATE.get("patched_modules", []):
        try:
            setattr(module, attr, orig)
        except (AttributeError, TypeError):
            continue

    _PATCH_STATE["installed"] = False
    _PATCH_STATE["patched_modules"] = []
    _PATCH_STATE["replaced_locations"] = []
    _stop_global_progress()
