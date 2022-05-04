import sys
from unittest.mock import call, create_autospec

import pytest

try:
    from rich._win32_console import LegacyWindowsTerm, WindowsCoordinates
    from rich._windows_renderer import legacy_windows_render
except:
    # These modules can only be imported on Windows
    pass
from rich.segment import ControlType, Segment
from rich.style import Style

pytestmark = pytest.mark.skipif(sys.platform != "win32", reason="windows only")


@pytest.fixture
def legacy_term_mock():
    return create_autospec(LegacyWindowsTerm)


def test_text_only(legacy_term_mock):
    text = "Hello, world!"
    buffer = [Segment(text)]
    legacy_windows_render(buffer, legacy_term_mock)

    legacy_term_mock.write_text.assert_called_once_with(text)


def test_text_multiple_segments(legacy_term_mock):
    buffer = [Segment("Hello, "), Segment("world!")]
    legacy_windows_render(buffer, legacy_term_mock)

    assert legacy_term_mock.write_text.call_args_list == [
        call("Hello, "),
        call("world!"),
    ]


def test_text_with_style(legacy_term_mock):
    text = "Hello, world!"
    style = Style.parse("black on red")
    buffer = [Segment(text, style)]

    legacy_windows_render(buffer, legacy_term_mock)

    legacy_term_mock.write_styled.assert_called_once_with(text, style)


def test_control_cursor_move_to(legacy_term_mock):
    buffer = [Segment("", None, [(ControlType.CURSOR_MOVE_TO, 20, 30)])]

    legacy_windows_render(buffer, legacy_term_mock)

    legacy_term_mock.move_cursor_to.assert_called_once_with(
        WindowsCoordinates(row=29, col=19)
    )


def test_control_carriage_return(legacy_term_mock):
    buffer = [Segment("", None, [(ControlType.CARRIAGE_RETURN,)])]

    legacy_windows_render(buffer, legacy_term_mock)

    legacy_term_mock.write_text.assert_called_once_with("\r")


def test_control_home(legacy_term_mock):
    buffer = [Segment("", None, [(ControlType.HOME,)])]

    legacy_windows_render(buffer, legacy_term_mock)

    legacy_term_mock.move_cursor_to.assert_called_once_with(WindowsCoordinates(0, 0))


@pytest.mark.parametrize(
    "control_type, method_name",
    [
        (ControlType.CURSOR_UP, "move_cursor_up"),
        (ControlType.CURSOR_DOWN, "move_cursor_down"),
        (ControlType.CURSOR_FORWARD, "move_cursor_forward"),
        (ControlType.CURSOR_BACKWARD, "move_cursor_backward"),
    ],
)
def test_control_cursor_single_cell_movement(
    legacy_term_mock, control_type, method_name
):
    buffer = [Segment("", None, [(control_type,)])]

    legacy_windows_render(buffer, legacy_term_mock)

    getattr(legacy_term_mock, method_name).assert_called_once_with()


@pytest.mark.parametrize(
    "erase_mode, method_name",
    [
        (0, "erase_end_of_line"),
        (1, "erase_start_of_line"),
        (2, "erase_line"),
    ],
)
def test_control_erase_line(legacy_term_mock, erase_mode, method_name):
    buffer = [Segment("", None, [(ControlType.ERASE_IN_LINE, erase_mode)])]

    legacy_windows_render(buffer, legacy_term_mock)

    getattr(legacy_term_mock, method_name).assert_called_once_with()


def test_control_show_cursor(legacy_term_mock):
    buffer = [Segment("", None, [(ControlType.SHOW_CURSOR,)])]

    legacy_windows_render(buffer, legacy_term_mock)

    legacy_term_mock.show_cursor.assert_called_once_with()


def test_control_hide_cursor(legacy_term_mock):
    buffer = [Segment("", None, [(ControlType.HIDE_CURSOR,)])]

    legacy_windows_render(buffer, legacy_term_mock)

    legacy_term_mock.hide_cursor.assert_called_once_with()


def test_control_cursor_move_to_column(legacy_term_mock):
    buffer = [Segment("", None, [(ControlType.CURSOR_MOVE_TO_COLUMN, 3)])]

    legacy_windows_render(buffer, legacy_term_mock)

    legacy_term_mock.move_cursor_to_column.assert_called_once_with(2)


def test_control_set_terminal_window_title(legacy_term_mock):
    buffer = [Segment("", None, [(ControlType.SET_WINDOW_TITLE, "Hello, world!")])]

    legacy_windows_render(buffer, legacy_term_mock)

    legacy_term_mock.set_title.assert_called_once_with("Hello, world!")
