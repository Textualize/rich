from rich.control import Control, strip_control_codes
from rich.segment import ControlType


def test_control():
    control = Control(ControlType.BELL)
    assert str(control) == "\x07"


def test_strip_control_codes():
    assert strip_control_codes("") == ""
    assert strip_control_codes("foo\rbar") == "foobar"
    assert strip_control_codes("Fear is the mind killer") == "Fear is the mind killer"
