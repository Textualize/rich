"""
Safe markup output — escaping user content before writing to a Rich console.

When displaying data from external sources (API responses, tool output, database
records) you must escape the content before passing it to Rich's markup parser,
otherwise brackets in the data are interpreted as markup tags.

Use ``rich.markup.escape`` for this.
"""

from rich.console import Console
from rich.markup import escape
from rich.panel import Panel
from rich.table import Table

console = Console()

# ── Bad: user content passed directly ───────────────────────────────────────
# If content contains "[red]" or "[bold]" these are parsed as markup tags,
# which can raise exceptions or produce unintended formatting.

user_content = "Error: [Errno 2] No such file or directory: '/tmp/data.json'"
sql_result = "SELECT * FROM users WHERE name='[admin]'"
api_payload = '{"status": "[ok]", "msg": "record [1] saved"}'

# ── Good: escape before rendering ───────────────────────────────────────────
console.print(Panel(escape(user_content), title="File error", border_style="red"))
console.print(Panel(escape(sql_result), title="Query", border_style="blue"))
console.print(Panel(escape(api_payload), title="API response", border_style="green"))

# ── In a table ───────────────────────────────────────────────────────────────
records = [
    ("users/1", '{"name": "[admin]", "role": "superuser"}'),
    ("logs/42", "Process [A] exited with code [1]"),
    ("queue/7", "[task] write /etc/hosts [priority=high]"),
]

table = Table(title="Store records", show_lines=True)
table.add_column("ID", style="dim")
table.add_column("Content")  # content is escaped before adding

for record_id, content in records:
    table.add_row(escape(record_id), escape(content))

console.print(table)

# ── In a formatted string ─────────────────────────────────────────────────────
# Use f-strings only after escaping individual variables.
name = "O'Brien [admin]"
console.print(f"[bold]User:[/bold] {escape(name)}")

# ── Highlight mode ─────────────────────────────────────────────────────────────
# Console(highlight=True) auto-formats numbers, strings, etc. in repr output
# but still requires markup.escape for user-controlled strings in markup context.
debug_console = Console(highlight=True)
debug_console.print(escape('{"key": "[value]", "count": 42}'))
