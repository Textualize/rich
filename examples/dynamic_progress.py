"""

Demonstrates how to create a dynamic group of progress bars,
showing multi-level progress for multiple tasks (installing apps in the example),
each of which consisting of multiple steps.

"""

import time

from rich.console import Group
from rich.live import Live
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)


def run_steps(name, step_times, app_steps_task_id):
    """Run steps for a single app, and update corresponding progress bars."""

    for idx, step_time in enumerate(step_times):
        # add progress bar for this step (time elapsed + spinner)
        action = step_actions[idx]
        step_task_id = step_progress.add_task("", action=action, name=name)

        # run steps, update progress
        for _ in range(step_time):
            time.sleep(0.5)
            step_progress.update(step_task_id, advance=1)

        # stop and hide progress bar for this step when done
        step_progress.stop_task(step_task_id)
        step_progress.update(step_task_id, visible=False)

        # also update progress bar for current app when step is done
        app_steps_progress.update(app_steps_task_id, advance=1)


# progress bar for current app showing only elapsed time,
# which will stay visible when app is installed
current_app_progress = Progress(
    TimeElapsedColumn(),
    TextColumn("{task.description}"),
)

# progress bars for single app steps (will be hidden when step is done)
step_progress = Progress(
    TextColumn("  "),
    TimeElapsedColumn(),
    TextColumn("[bold purple]{task.fields[action]}"),
    SpinnerColumn("simpleDots"),
)
# progress bar for current app (progress in steps)
app_steps_progress = Progress(
    TextColumn(
        "[bold blue]Progress for app {task.fields[name]}: {task.percentage:.0f}%"
    ),
    BarColumn(),
    TextColumn("({task.completed} of {task.total} steps done)"),
)
# overall progress bar
overall_progress = Progress(
    TimeElapsedColumn(), BarColumn(), TextColumn("{task.description}")
)
# group of progress bars;
# some are always visible, others will disappear when progress is complete
progress_group = Group(
    Panel(Group(current_app_progress, step_progress, app_steps_progress)),
    overall_progress,
)

# tuple specifies how long each step takes for that app
step_actions = ("downloading", "configuring", "building", "installing")
apps = [
    ("one", (2, 1, 4, 2)),
    ("two", (1, 3, 8, 4)),
    ("three", (2, 1, 3, 2)),
]

# create overall progress bar
overall_task_id = overall_progress.add_task("", total=len(apps))

# use own live instance as context manager with group of progress bars,
# which allows for running multiple different progress bars in parallel,
# and dynamically showing/hiding them
with Live(progress_group):

    for idx, (name, step_times) in enumerate(apps):
        # update message on overall progress bar
        top_descr = "[bold #AAAAAA](%d out of %d apps installed)" % (idx, len(apps))
        overall_progress.update(overall_task_id, description=top_descr)

        # add progress bar for steps of this app, and run the steps
        current_task_id = current_app_progress.add_task("Installing app %s" % name)
        app_steps_task_id = app_steps_progress.add_task(
            "", total=len(step_times), name=name
        )
        run_steps(name, step_times, app_steps_task_id)

        # stop and hide steps progress bar for this specific app
        app_steps_progress.update(app_steps_task_id, visible=False)
        current_app_progress.stop_task(current_task_id)
        current_app_progress.update(
            current_task_id, description="[bold green]App %s installed!" % name
        )

        # increase overall progress now this task is done
        overall_progress.update(overall_task_id, advance=1)

    # final update for message on overall progress bar
    overall_progress.update(
        overall_task_id, description="[bold green]%s apps installed, done!" % len(apps)
    )
