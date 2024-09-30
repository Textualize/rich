"""Lite simulation of the top linux command."""
import datetime
import random
import sys
import time
from dataclasses import dataclass

from rich import box
from rich.console import Console
from rich.live import Live
from rich.table import Table

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


@dataclass
class Process:
    pid: int
    command: str
    cpu_percent: float
    memory: int
    start_time: datetime.datetime
    thread_count: int
    state: Literal["running", "sleeping"]

    @property
    def memory_str(self) -> str:
        if self.memory > 1e6:
            return f"{int(self.memory/1e6)}M"
        if self.memory > 1e3:
            return f"{int(self.memory/1e3)}K"
        return str(self.memory)

    @property
    def time_str(self) -> str:
        return str(datetime.datetime.now() - self.start_time)


def generate_process(pid: int) -> Process:
    return Process(
        pid=pid,
        command=f"Process {pid}",
        cpu_percent=random.random() * 20,
        memory=random.randint(10, 200) ** 3,
        start_time=datetime.datetime.now()
        - datetime.timedelta(seconds=random.randint(0, 500) ** 2),
        thread_count=random.randint(1, 32),
        state="running" if random.randint(0, 10) < 8 else "sleeping",
    )


def create_process_table(height: int) -> Table:
    processes = sorted(
        [generate_process(pid) for pid in range(height)],
        key=lambda p: p.cpu_percent,
        reverse=True,
    )
    table = Table(
        "PID", "Command", "CPU %", "Memory", "Time", "Thread #", "State", box=box.SIMPLE
    )

    for process in processes:
        table.add_row(
            str(process.pid),
            process.command,
            f"{process.cpu_percent:.1f}",
            process.memory_str,
            process.time_str,
            str(process.thread_count),
            process.state,
        )

    return table


console = Console()

with Live(console=console, screen=True, auto_refresh=False) as live:
    while True:
        live.update(create_process_table(console.size.height - 4), refresh=True)
        time.sleep(1)
