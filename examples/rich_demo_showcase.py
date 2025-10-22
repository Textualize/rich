"""
Rich Library Demo - Exploring Features
Made by: Yaroslav Voryk
For: Open Source Software Assignment

This is my demo showing what I learned about the Rich library!
I tried out different features to see what this library can do.
"""

from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.syntax import Syntax
from rich.panel import Panel
from rich.tree import Tree
from rich.markdown import Markdown
from rich.columns import Columns
from rich.layout import Layout
from rich.live import Live
from rich import box
from rich.text import Text
from rich.json import JSON
from rich.pretty import Pretty
from rich.rule import Rule
import time
import json

# Create a console object - this is what we use to print stuff
console = Console()

def intro():
    """Simple intro to my demo"""
    console.clear()
    console.print("\n")
    
    # Making a cool title with different colors
    title = Text()
    title.append("R", style="bold red")
    title.append("I", style="bold yellow")
    title.append("C", style="bold green")
    title.append("H", style="bold cyan")
    title.append(" ", style="bold")
    title.append("L", style="bold blue")
    title.append("I", style="bold magenta")
    title.append("B", style="bold red")
    title.append("R", style="bold yellow")
    title.append("A", style="bold green")
    title.append("R", style="bold cyan")
    title.append("Y", style="bold blue")
    title.append(" ", style="bold")
    title.append("D", style="bold magenta")
    title.append("E", style="bold red")
    title.append("M", style="bold yellow")
    title.append("O", style="bold green")
    
    console.print(title, justify="center")
    console.print("[dim]by Yaroslav Voryk - Testing out cool features![/dim]", justify="center")
    console.print("=" * 70, style="cyan")
    console.print()
    time.sleep(0.5)

def test_text_styles():
    """First thing I tried - styling text!"""
    console.print(Rule("[bold cyan]1. TEXT STYLING & COLORS", style="cyan"))
    console.print()
    
    # Testing basic styles
    console.print("[yellow]Basic text styling I figured out:[/yellow]")
    console.print("  [bold]This is bold[/bold]")
    console.print("  [italic]This is italic[/italic]")
    console.print("  [underline]This is underlined[/underline]")
    console.print("  [strike]Strikethrough![/strike]")
    console.print()
    
    # Testing colors - this is cool!
    console.print("[yellow]All the colors:[/yellow]")
    console.print("  [red]Red[/red] [green]Green[/green] [blue]Blue[/blue] [yellow]Yellow[/yellow] [magenta]Magenta[/magenta] [cyan]Cyan[/cyan]")
    console.print()
    
    # You can combine them!
    console.print("[yellow]Combining styles (this is my favorite part!):[/yellow]")
    console.print("  [bold red]Bold and Red[/bold red]")
    console.print("  [italic green]Italic and Green[/italic green]")
    console.print("  [bold yellow on blue]Yellow text on blue background[/bold yellow on blue]")
    
    # Status indicators - useful for projects!
    console.print()
    console.print("[yellow]Status indicators I made:[/yellow]")
    console.print("  [bold white on green] SUCCESS [/bold white on green] Everything worked!")
    console.print("  [bold white on yellow] WARNING [/bold white on yellow] Be careful here")
    console.print("  [bold white on red] ERROR [/bold white on red] Something broke")
    console.print("\n")

def test_tables():
    """Tables are pretty useful for displaying data"""
    console.print(Rule("[bold cyan]2. TABLES & DATA", style="cyan"))
    console.print()
    
    # Made a table with my class schedule
    table = Table(title="My Fall 2024 Schedule", box=box.ROUNDED, show_lines=True)
    
    table.add_column("Course", style="cyan", width=15)
    table.add_column("Professor", style="green", width=15)
    table.add_column("Time", style="yellow", width=15)
    table.add_column("Grade", style="magenta", justify="center", width=8)
    
    table.add_row("Open Source", "Prof. Smith", "MWF 10:00", "[green]A[/green]")
    table.add_row("Data Structures", "Prof. Johnson", "TR 14:00", "[yellow]B+[/yellow]")
    table.add_row("Web Dev", "Prof. Lee", "MW 16:00", "[green]A-[/green]")
    table.add_row("Algorithms", "Prof. Davis", "TR 10:00", "[yellow]B[/yellow]")
    
    console.print(table)
    console.print()
    
    # Project status table - I use this to track my assignments!
    console.print("[yellow]My project tracker:[/yellow]\n")
    table2 = Table(box=box.SIMPLE_HEAD)
    table2.add_column("Project", style="cyan")
    table2.add_column("Status", justify="center", width=15)
    table2.add_column("Due Date", style="yellow")
    
    table2.add_row("Rich Demo", "[bold green]DONE![/bold green]", "Oct 22")
    table2.add_row("Web App", "[yellow]In Progress[/yellow]", "Oct 30")
    table2.add_row("Final Project", "[red]Not Started[/red]", "Dec 15")
    
    console.print(table2)
    console.print("\n")

def test_progress():
    """Progress bars - these are really cool for showing loading"""
    console.print(Rule("[bold cyan]3. PROGRESS BARS", style="cyan"))
    console.print()
    
    console.print("[yellow]Testing different progress styles:[/yellow]\n")
    
    # Multiple progress bars at once - this looks so cool!
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    ) as progress:
        
        task1 = progress.add_task("[cyan]Downloading files...", total=100)
        task2 = progress.add_task("[green]Processing data...", total=100)
        task3 = progress.add_task("[magenta]Running tests...", total=100)
        
        while not progress.finished:
            progress.update(task1, advance=3)
            progress.update(task2, advance=2)
            progress.update(task3, advance=1.5)
            time.sleep(0.02)
    
    console.print("\n[bold green]All tasks complete![/bold green]\n")

def test_code_highlighting():
    """This feature is awesome - it highlights code!"""
    console.print(Rule("[bold cyan]4. CODE SYNTAX HIGHLIGHTING", style="cyan"))
    console.print()
    
    # Here's some code I wrote for my data structures class
    my_code = '''
class Student:
    """
    Student class I made for my database project
    """
    def __init__(self, name, student_id, gpa):
        self.name = name
        self.student_id = student_id
        self.gpa = gpa
        self.courses = []
    
    def add_course(self, course):
        """Add a course to the student's schedule"""
        self.courses.append(course)
        print(f"{self.name} enrolled in {course}")
    
    def get_info(self):
        """Display student information"""
        return f"Student: {self.name} (ID: {self.student_id}) - GPA: {self.gpa}"

# Testing the class
student = Student("Yaroslav", "12345", 3.8)
student.add_course("Open Source Software")
print(student.get_info())
'''
    
    # Rich can highlight it automatically!
    syntax = Syntax(my_code, "python", theme="monokai", line_numbers=True)
    console.print(Panel(syntax, title="[yellow]My Student Class", border_style="yellow"))
    console.print("\n")

def test_tree_structure():
    """Tree structures - good for showing file hierarchies"""
    console.print(Rule("[bold cyan]5. TREE STRUCTURE", style="cyan"))
    console.print()
    
    console.print("[yellow]Here's how my semester projects are organized:[/yellow]\n")
    
    # Creating a tree - this looks really professional!
    tree = Tree("[bold blue]Fall_2024_Projects/")
    
    # Open Source assignment
    opensource = tree.add("[bold yellow]OpenSource_Assignment/")
    opensource.add("[green]rich_demo.py [dim]- this file![/dim]")
    opensource.add("[green]video_script.md [dim]- presentation script[/dim]")
    opensource.add("[green]analysis.md [dim]- project analysis[/dim]")
    
    # Web Dev project
    webdev = tree.add("[bold yellow]WebDev_Project/")
    frontend = webdev.add("[yellow]frontend/")
    frontend.add("[green]index.html")
    frontend.add("[green]style.css")
    frontend.add("[green]app.js")
    backend = webdev.add("[yellow]backend/")
    backend.add("[green]server.py")
    backend.add("[green]database.py")
    
    # Data Structures homework
    ds = tree.add("[bold yellow]DataStructures_HW/")
    ds.add("[green]linked_list.py [dim]- Assignment 3[/dim]")
    ds.add("[green]binary_tree.py [dim]- Assignment 4[/dim]")
    ds.add("[green]graph.py [dim]- Assignment 5[/dim]")
    
    tree.add("[cyan]README.md [dim]- portfolio notes[/dim]")
    
    console.print(tree)
    console.print("\n")

def test_live_display():
    """Live updating display - this is SO cool!"""
    console.print(Rule("[bold cyan]6. LIVE UPDATES", style="cyan"))
    console.print()
    
    console.print("[yellow]Watch this live counter (testing real-time updates):[/yellow]\n")
    
    # Create a live updating table
    with Live(console=console, refresh_per_second=10) as live:
        for i in range(15):
            # Create a new table each iteration
            table = Table(box=box.ROUNDED)
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="green", justify="right")
            
            table.add_row("Counter", f"{i + 1}")
            table.add_row("Progress", f"{((i + 1) / 15) * 100:.1f}%")
            table.add_row("Status", "[green]Running...[/green]" if i < 14 else "[bold green]Complete![/bold green]")
            
            live.update(Panel(table, title="[bold]Live Status Monitor", border_style="cyan"))
            time.sleep(0.15)
    
    console.print("\n[green]Live update test complete![/green]\n")

def test_json_pretty():
    """JSON and pretty printing - useful for API projects"""
    console.print(Rule("[bold cyan]7. JSON & DATA DISPLAY", style="cyan"))
    console.print()
    
    # Sample API response I'm working with in my web dev class
    api_data = {
        "user": {
            "id": 12345,
            "name": "Yaroslav Voryk",
            "email": "yvoryk@university.edu",
            "major": "Computer Science",
            "year": "Junior",
            "courses": ["CIS4930", "COP3530", "COP3014"],
            "gpa": 3.8,
            "enrolled": True
        },
        "semester": "Fall 2024",
        "credits": 15,
        "status": "active"
    }
    
    console.print("[yellow]Testing JSON display (from my web API project):[/yellow]\n")
    json_display = JSON(json.dumps(api_data), indent=2)
    console.print(Panel(json_display, title="[cyan]API Response", border_style="cyan"))
    console.print("\n")

def test_panels_layouts():
    """Panels and boxes - for organizing information"""
    console.print(Rule("[bold cyan]8. PANELS & LAYOUTS", style="cyan"))
    console.print()
    
    # Dashboard-style layout
    console.print("[yellow]Made a dashboard layout:[/yellow]\n")
    
    # Three column system
    col1 = Panel(
        "[bold green]My Stats[/bold green]\n\n"
        "Classes: [cyan]4[/cyan]\n"
        "Projects: [cyan]8[/cyan]\n"
        "GPA: [cyan]3.8[/cyan]\n"
        "Hours Studied: [cyan]120+[/cyan]",
        border_style="green",
        box=box.ROUNDED
    )
    
    col2 = Panel(
        "[bold yellow]This Week[/bold yellow]\n\n"
        "Assignments: [cyan]3[/cyan]\n"
        "Tests: [cyan]1[/cyan]\n"
        "Study Groups: [cyan]2[/cyan]\n"
        "Free Time: [red]0[/red]",
        border_style="yellow",
        box=box.ROUNDED
    )
    
    col3 = Panel(
        "[bold magenta]To Do[/bold magenta]\n\n"
        "[green]x[/green] Rich Demo\n"
        "[ ] Web App UI\n"
        "[ ] Study for test\n"
        "[ ] Group project",
        border_style="magenta",
        box=box.ROUNDED
    )
    
    console.print(Columns([col1, col2, col3], equal=True, expand=True))
    console.print()
    
    # Info panel
    info_panel = Panel(
        "[bold cyan]What I Learned About Rich:[/bold cyan]\n\n"
        " [green]+[/green] Super easy to add colors and styles\n"
        " [green]+[/green] Makes my terminal output look professional\n"
        " [green]+[/green] Perfect for CLI projects and assignments\n"
        " [green]+[/green] Live updates are amazing!\n"
        " [green]+[/green] Great documentation and examples\n"
        " [green]+[/green] Way better than using print() everywhere",
        title="[bold yellow]My Notes",
        subtitle="[dim]Would definitely use this again!",
        border_style="blue",
        box=box.DOUBLE
    )
    console.print(info_panel)
    console.print("\n")

def test_markdown():
    """Rich can even render markdown!"""
    console.print(Rule("[bold cyan]9. MARKDOWN RENDERING", style="cyan"))
    console.print()
    
    # My project README
    my_markdown = """
# My Open Source Project Analysis

## What I Did:
1. Explored the **Rich** library on GitHub
2. Read through the documentation
3. Cloned and ran the project locally  
4. Tested out different features
5. Made this demo!

## Key Features I Tested:
- **Text styling** - colors, bold, italic
- **Tables** - for displaying data
- **Progress bars** - for loading indicators
- `Code highlighting` - with line numbers
- **Live updates** - real-time displays

## My Thoughts:
This library is *really* useful! I can see myself using it for:
- Class projects
- Personal CLI tools
- Data visualization
- Log formatting

```python
# Super easy to use!
from rich.console import Console
console = Console()
console.print("[bold green]Hello World![/bold green]")
```

**Rating:** 10/10 would recommend!
"""
    
    md = Markdown(my_markdown)
    console.print(Panel(md, border_style="blue", box=box.ROUNDED, padding=(1, 1)))
    console.print("\n")

def test_logging_example():
    """Logging feature - useful for debugging"""
    console.print(Rule("[bold cyan]10. LOGGING EXAMPLE", style="cyan"))
    console.print()
    
    console.print("[yellow]Testing different log levels (for my debugging):[/yellow]\n")
    
    # Simulating a program running with logs
    console.log("[cyan]INFO:[/cyan] Starting application...")
    time.sleep(0.3)
    console.log("[green]SUCCESS:[/green] Connected to database")
    time.sleep(0.3)
    console.log("[cyan]INFO:[/cyan] Loading user data...")
    time.sleep(0.3)
    console.log("[yellow]WARNING:[/yellow] Cache miss, fetching from database")
    time.sleep(0.3)
    console.log("[green]SUCCESS:[/green] User authenticated")
    time.sleep(0.3)
    console.log("[cyan]INFO:[/cyan] Processing request...")
    time.sleep(0.3)
    console.log("[red]ERROR:[/red] Network timeout - retrying...")
    time.sleep(0.3)
    console.log("[green]SUCCESS:[/green] Request completed successfully")
    
    console.print("\n[green]Logging example complete![/green]\n")

def show_summary():
    """Wrap up the demo"""
    console.print("\n")
    console.print("=" * 70, style="bold cyan")
    console.print()
    
    summary = Table(box=None, show_header=False, padding=(0, 2))
    summary.add_column(style="bold yellow")
    summary.add_column(style="cyan")
    
    summary.add_row("Features Tested:", "10")
    summary.add_row("Lines of Code:", "~300")
    summary.add_row("Coolness Factor:", "[bold green]Very High![/bold green]")
    summary.add_row("Will Use Again:", "[bold green]Definitely![/bold green]")
    
    console.print(Panel(
        summary,
        title="[bold green]Demo Complete!",
        subtitle="[dim]Thanks for watching!",
        border_style="green"
    ))
    
    console.print()
    console.print("[cyan]Perfect for my future CLI projects and assignments![/cyan]", justify="center")
    console.print()
    console.print("=" * 70, style="bold cyan")
    console.print()

def main():
    """Run all my tests"""
    try:
        intro()
        test_text_styles()
        test_tables()
        test_progress()
        test_code_highlighting()
        test_tree_structure()
        test_live_display()
        test_json_pretty()
        test_panels_layouts()
        test_markdown()
        test_logging_example()
        show_summary()
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Demo stopped[/yellow]")

if __name__ == "__main__":
    main()
