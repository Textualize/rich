"""Tests for pickle support in Rich objects."""

import pickle
from rich.console import Console, ConsoleThreadLocals
from rich.segment import Segment
from rich.theme import Theme, ThemeStack


def test_console_thread_locals_pickle():
    """Test that ConsoleThreadLocals can be pickled and unpickled."""
    console = Console()
    ctl = console._thread_locals

    # Add some data to make it more realistic
    ctl.buffer.append(Segment("test"))
    ctl.buffer_index = 1

    # Test serialization
    pickled_data = pickle.dumps(ctl)

    # Test deserialization
    restored_ctl = pickle.loads(pickled_data)

    # Verify state preservation
    assert type(restored_ctl.theme_stack) == type(ctl.theme_stack)
    assert restored_ctl.buffer == ctl.buffer
    assert restored_ctl.buffer_index == ctl.buffer_index


def test_console_pickle():
    """Test that Console objects can be pickled and unpickled."""
    console = Console(width=120, height=40)

    # Test serialization
    pickled_data = pickle.dumps(console)

    # Test deserialization
    restored_console = pickle.loads(pickled_data)

    # Verify basic properties are preserved
    assert restored_console.width == console.width
    assert restored_console.height == console.height
    assert restored_console._color_system == console._color_system

    # Verify locks are recreated
    assert hasattr(restored_console, "_lock")
    assert hasattr(restored_console, "_record_buffer_lock")

    # Verify the console is functional
    with restored_console.capture() as capture:
        restored_console.print("Test message")

    assert "Test message" in capture.get()


def test_console_with_complex_state_pickle():
    """Test console pickle with more complex state."""
    theme = Theme({"info": "cyan", "warning": "yellow", "error": "red bold"})

    console = Console(theme=theme, record=True)

    # Add some content
    console.print("Info message", style="info")
    console.print("Warning message", style="warning")
    console.record = False  # Stop recording

    # Test serialization
    pickled_data = pickle.dumps(console)

    # Test deserialization
    restored_console = pickle.loads(pickled_data)

    # Verify theme is preserved
    assert restored_console.get_style("info").color.name == "cyan"
    assert restored_console.get_style("warning").color.name == "yellow"

    # Verify console functionality
    assert restored_console.record is False


def test_cache_simulation():
    """Test cache-like usage scenario (similar to Langflow)."""
    console = Console()

    # Simulate caching scenario like Langflow
    cache_data = {
        "result": console,
        "type": type(console),
        "metadata": {"created": "2025-09-25", "version": "1.0"},
    }

    # This should not raise any pickle errors
    pickled = pickle.dumps(cache_data)
    restored = pickle.loads(pickled)

    # Verify restoration
    assert type(restored["result"]) == Console
    assert restored["type"] == Console
    assert restored["metadata"]["created"] == "2025-09-25"

    # Verify the restored console works
    restored_console = restored["result"]
    with restored_console.capture() as capture:
        restored_console.print("Cache test successful")

    assert "Cache test successful" in capture.get()


def test_nested_console_pickle():
    """Test pickling dict containing Console instances."""
    # Use a simple dict instead of local class to avoid pickle issues
    container = {
        "console": Console(width=100),
        "name": "test_container",
        "data": [1, 2, 3],
    }

    # Should be able to pickle dict containing Console
    pickled = pickle.dumps(container)
    restored = pickle.loads(pickled)

    assert restored["name"] == "test_container"
    assert restored["data"] == [1, 2, 3]
    assert restored["console"].width == 100

    # Verify console functionality
    with restored["console"].capture() as capture:
        restored["console"].print("Nested test")

    assert "Nested test" in capture.get()


if __name__ == "__main__":
    # Run tests manually if called directly
    import sys

    tests = [
        test_console_thread_locals_pickle,
        test_console_pickle,
        test_console_with_complex_state_pickle,
        test_cache_simulation,
        test_nested_console_pickle,
    ]

    passed = 0
    for test in tests:
        try:
            test()
            print(f"✅ {test.__name__} passed")
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__} failed: {e}")

    print(f"\n📊 Results: {passed}/{len(tests)} tests passed")
    sys.exit(0 if passed == len(tests) else 1)
