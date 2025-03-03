from time import sleep
from rich.panel import Panel
from rich.progress import Progress


JOBS = [100, 150, 25, 70, 110, 90]

progress = Progress(auto_refresh=False)
jobs_task = progress.add_task("jobs")
master_task = progress.add_task("Overall", total=sum(JOBS))

progress.console.print(
    Panel(
        "[bold blue]A demonstration of progress with a current task and overall progress.",
        padding=1,
    )
)

with progress:
    for job_no, job in enumerate(JOBS):
        progress.log(f"Starting job #{job_no}")
        sleep(0.2)
        progress.reset(jobs_task, total=job, description=f"Job [bold yellow]#{job_no}")
        progress.start_task(jobs_task)
        for wait in progress.track(range(job), task_id=jobs_task):
            sleep(0.01)
        progress.advance(master_task, job)
        progress.log(f"Finished job #{job_no}")

progress.console.print(
    Panel(":sparkle: All done! :sparkle:", border_style="green", padding=1)
)
