from rich.console import Console


def test_jupyter():
    console = Console(force_jupyter=True)
    assert console.width == 115
    assert console.height == 100
    assert console.color_system == "truecolor"


def test_jupyter_columns_env():
    console = Console(_environ={"JUPYTER_COLUMNS": "314"}, force_jupyter=True)
    assert console.width == 314
    # width take precedence
    console = Console(width=40, _environ={"JUPYTER_COLUMNS": "314"}, force_jupyter=True)
    assert console.width == 40
    # Should not fail
    console = Console(
        width=40, _environ={"JUPYTER_COLUMNS": "broken"}, force_jupyter=True
    )


def test_jupyter_lines_env():
    console = Console(_environ={"JUPYTER_LINES": "220"}, force_jupyter=True)
    assert console.height == 220
    # height take precedence
    console = Console(height=40, _environ={"JUPYTER_LINES": "220"}, force_jupyter=True)
    assert console.height == 40
    # Should not fail
    console = Console(
        width=40, _environ={"JUPYTER_LINES": "broken"}, force_jupyter=True
    )
