"""

Demonstrates the use of multiple Progress instances in a single Live display.

"""

from time import sleep

from rich.live import Live
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.table import Table

job_progress = Progress(
    "{task.description}",
    SpinnerColumn(),
    BarColumn(),
    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
)
job1 = job_progress.add_task("[green]Cooking")
job2 = job_progress.add_task("[magenta]Baking", total=200)
job3 = job_progress.add_task("[cyan]Mixing", total=400)

total = sum(task.total for task in job_progress.tasks)
overall_progress = Progress()
overall_task = overall_progress.add_task("All Jobs", total=int(total))

progress_table = Table.grid()
progress_table.add_row(
    Panel.fit(
        overall_progress, title="Overall Progress", border_style="green", padding=(2, 2)
    ),
    Panel.fit(job_progress, title="[b]Jobs", border_style="red", padding=(1, 2)),
)

with Live(progress_table, refresh_per_second=10):
    while not overall_progress.finished:
        sleep(0.1)
        for job in job_progress.tasks:
            if not job.finished:
                job_progress.advance(job.id)

        completed = sum(task.completed for task in job_progress.tasks)
        overall_progress.update(overall_task, completed=completed)
