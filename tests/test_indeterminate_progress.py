"""Tests for indeterminate progress bar functionality."""

import time
import pytest
from rich.console import Console
from rich.progress import (
    Progress,
    Task,
    BarColumn,
    TimeElapsedColumn,
    IndeterminateTaskProgressColumn,
    TaskProgressColumn,
)
from rich.table import Table
from rich.text import Text
from typing import Dict, Any
from threading import RLock


def test_indeterminate_task_creation():
    """Test that indeterminate tasks can be created with proper attributes."""
    progress = Progress()
    
    # Test indeterminate task with expected total
    task_id = progress.add_task("Test", indeterminate=True, expected_total=10)
    task = progress._tasks[task_id]
    
    assert task.indeterminate is True
    assert task.expected_total == 10
    assert task.total == 100.0  # Should have default total


def test_indeterminate_task_progress_column():
    """Test that IndeterminateTaskProgressColumn shows ?/total for indeterminate tasks."""
    column = IndeterminateTaskProgressColumn()
    
    # Create mock tasks
    indeterminate_task = Task(
        id=0,
        description="Test",
        total=None,
        completed=0,
        _get_time=time.monotonic,
        indeterminate=True,
        expected_total=10
    )
    
    regular_task = Task(
        id=1,
        description="Regular",
        total=100,
        completed=50,
        _get_time=time.monotonic,
        indeterminate=False
    )
    
    # Test rendering for indeterminate task
    result = column.render(indeterminate_task)
    assert str(result) == "?/10"
    
    # Test rendering for regular task
    result = column.render(regular_task)
    assert str(result) == "50/100"


def test_indeterminate_with_elapsed_time():
    """Test that indeterminate progress bars show elapsed time."""
    progress = Progress(
        BarColumn(),
        TimeElapsedColumn(),
    )
    
    task_id = progress.add_task("Test", indeterminate=True)
    task = progress._tasks[task_id]
    
    # Simulate time passing (use the task's get_time method)
    task.start_time = task.get_time() - 5.0
    
    assert task.elapsed > 0
    assert task.should_show_indeterminate is True


def test_indeterminate_to_determinate_transition():
    """Test transitioning from indeterminate to determinate state."""
    progress = Progress()
    
    # Start with indeterminate
    task_id = progress.add_task("Test", indeterminate=True, expected_total=10)
    task = progress._tasks[task_id]
    
    assert task.indeterminate is True
    assert task.should_show_indeterminate is True
    
    # Transition to determinate (directly modify the task)
    task.indeterminate = False
    task.total = 10
    task.completed = 10
    
    assert task.indeterminate is False
    assert task.total == 10
    assert task.completed == 10
    assert task.should_show_indeterminate is False


def test_bar_column_indeterminate_animation():
    """Test that BarColumn creates animated display for indeterminate tasks."""
    bar_column = BarColumn()
    
    # Create an indeterminate task
    task = Task(
        id=0,
        description="Test",
        total=None,
        completed=0,
        _get_time=time.monotonic,
        indeterminate=True
    )
    task.start_time = time.monotonic()
    
    # Test that it renders without error
    result = bar_column.render(task)
    assert result is not None
    assert isinstance(result, (Text, Table))


@pytest.mark.parametrize("expected_total", [None, 10, 100])
def test_indeterminate_with_different_expected_totals(expected_total):
    """Test indeterminate tasks with various expected totals."""
    progress = Progress()
    
    task_id = progress.add_task(
        "Test",
        indeterminate=True,
        expected_total=expected_total
    )
    task = progress._tasks[task_id]
    
    assert task.indeterminate is True
    assert task.expected_total == expected_total
    
    # Test the progress column display
    column = IndeterminateTaskProgressColumn()
    result = column.render(task)
    
    if expected_total is None:
        assert str(result) == "?/?"
    else:
        assert str(result) == f"?/{expected_total}"


def test_visual_progress_bar_display(capsys):
    """Test the visual display of indeterminate progress bar."""
    console = Console(force_terminal=True, width=80, color_system="standard")
    
    with Progress(
        BarColumn(),
        TimeElapsedColumn(),
        console=console,
        transient=False,
    ) as progress:
        task_id = progress.add_task("Test", indeterminate=True)
        progress.refresh()
        
        # Check that something was rendered
        captured = capsys.readouterr()
        assert len(captured.out) > 0
        
        # The output should contain animation characters
        assert any(char in captured.out for char in ["━", "<<", ">>"])


def test_all_or_nothing_behavior():
    """Test the all-or-nothing behavior requested in issue #3572."""
    progress = Progress()
    
    # Create an indeterminate task
    task_id = progress.add_task(
        "Processing",
        indeterminate=True,
        expected_total=10
    )
    task = progress._tasks[task_id]
    
    # Verify it's in indeterminate state
    assert task.indeterminate is True
    assert task.expected_total == 10
    
    # Suddenly complete it (all-or-nothing) - directly modify the task
    task.indeterminate = False
    task.total = 10
    task.completed = 10
    task.finished_time = task.get_time()  # Mark as finished
    
    # Verify it's now complete
    assert task.indeterminate is False
    assert task.total == 10
    assert task.completed == 10
    assert task.finished is True