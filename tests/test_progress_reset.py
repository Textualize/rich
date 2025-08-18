"""Test that progress bar tasks properly reset their running clocks."""

import time
import pytest
from rich.console import Console
from rich.progress import Progress, Task, TaskID, TimeElapsedColumn


def test_progress_reset_restarts_clock():
    """Test that reset() properly resets the task's elapsed time."""
    progress = Progress()
    
    # Add a task and start it
    task_id = progress.add_task("Test", total=100)
    task = progress._tasks[task_id]
    
    # Advance the task
    progress.update(task_id, advance=50)
    
    # Simulate some time passing
    time.sleep(0.1)
    elapsed_before_reset = task.elapsed
    assert elapsed_before_reset > 0
    
    # Reset the task
    progress.reset(task_id)
    
    # Check that start_time was reset
    assert task.start_time is not None
    assert task.stop_time is None
    assert task.completed == 0
    assert task.finished_time is None
    
    # Check that elapsed time is very small (close to 0)
    elapsed_after_reset = task.elapsed
    assert elapsed_after_reset < elapsed_before_reset
    assert elapsed_after_reset < 0.1  # Should be very small, accounting for test execution time


def test_progress_reset_with_start_false():
    """Test that reset() with start=False leaves start_time as None."""
    progress = Progress()
    
    # Add a task and start it
    task_id = progress.add_task("Test", total=100)
    task = progress._tasks[task_id]
    
    # Simulate some work
    progress.update(task_id, advance=50)
    time.sleep(0.1)
    
    # Reset without starting
    progress.reset(task_id, start=False)
    
    # Check that start_time is None
    assert task.start_time is None
    assert task.stop_time is None
    assert task.elapsed is None


def test_progress_reset_clears_stop_time():
    """Test that reset() clears stop_time to allow proper restart."""
    progress = Progress()
    
    # Add a task and start it
    task_id = progress.add_task("Test", total=100)
    task = progress._tasks[task_id]
    
    # Stop the task
    progress.stop_task(task_id)
    assert task.stop_time is not None
    
    # Reset the task
    progress.reset(task_id)
    
    # Check that stop_time was cleared
    assert task.stop_time is None
    assert task.start_time is not None


def test_progress_reset_scenario():
    """Test a realistic scenario with multiple progress bars being reset."""
    progress = Progress()
    
    # Simulate the AI training scenario from the bug report
    epoch_task = progress.add_task("Epochs", total=10)
    train_task = progress.add_task("Training", total=1000)
    valid_task = progress.add_task("Validation", total=500)
    
    # Simulate first epoch
    for _ in range(100):
        progress.advance(train_task, 10)
    
    progress.stop_task(train_task)
    
    for _ in range(50):
        progress.advance(valid_task, 10)
    
    progress.stop_task(valid_task)
    progress.advance(epoch_task, 1)
    
    # Reset tasks for next epoch
    progress.reset(train_task, start=True)
    progress.reset(valid_task, start=False)
    
    # Verify that training task has restarted properly
    train_task_obj = progress._tasks[train_task]
    assert train_task_obj.start_time is not None
    assert train_task_obj.stop_time is None
    assert train_task_obj.elapsed is not None
    assert train_task_obj.elapsed < 0.1  # Should be very small
    
    # Verify that validation task has not started
    valid_task_obj = progress._tasks[valid_task]
    assert valid_task_obj.start_time is None
    assert valid_task_obj.stop_time is None
    assert valid_task_obj.elapsed is None


def test_time_elapsed_column_after_reset():
    """Test that TimeElapsedColumn shows correct time after reset."""
    progress = Progress()
    column = TimeElapsedColumn()
    
    # Add a task and let it run
    task_id = progress.add_task("Test", total=100)
    task = progress._tasks[task_id]
    
    # Simulate work
    progress.update(task_id, advance=50)
    time.sleep(0.2)
    
    # Get elapsed time display before reset
    time_before = column.render(task)
    assert str(time_before) != "-:--:--"  # Should show actual time
    
    # Reset the task
    progress.reset(task_id)
    
    # Get elapsed time display after reset
    time_after = column.render(task)
    # Should show very small time or 0:00:00
    assert str(time_after) in ["0:00:00", "0:00:01"]