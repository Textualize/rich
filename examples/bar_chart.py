"""
Example of using BarChart to display data.

Run this example with:
    python examples/bar_chart.py
"""

from rich import print
from rich.bar_chart import BarChart
from rich.panel import Panel

# Example 1: Using a dictionary
print("\n[bold]Example 1: Sales Data (Dictionary)[/bold]")
sales_data = {
    "Q1": 45000,
    "Q2": 52000,
    "Q3": 48000,
    "Q4": 61000,
}
chart1 = BarChart(sales_data, width=50)
print(chart1)

# Example 2: Using a list of tuples
print("\n[bold]Example 2: Population by City (List of Tuples)[/bold]")
population_data = [
    ("Seoul", 9.7),
    ("Busan", 3.4),
    ("Incheon", 2.9),
    ("Daegu", 2.4),
    ("Daejeon", 1.5),
]
chart2 = BarChart(population_data, width=50, max_value=10.0)
print(chart2)

# Example 3: Using custom styles
print("\n[bold]Example 3: Custom Colors[/bold]")
chart3 = BarChart(
    {"Apples": 30, "Oranges": 25, "Bananas": 20, "Grapes": 15},
    width=50,
    bar_styles=["red", "yellow", "green", "magenta"],
    label_style="bold",
    value_style="dim",
)
print(chart3)

# Example 4: Without values
print("\n[bold]Example 4: Without Value Labels[/bold]")
chart4 = BarChart(
    {"Jan": 100, "Feb": 150, "Mar": 120, "Apr": 180},
    width=50,
    show_values=False,
    style="cyan",
)
print(chart4)

# Example 5: In a Panel
print("\n[bold]Example 5: Chart in a Panel[/bold]")
chart5 = BarChart(
    {"Python": 85, "JavaScript": 75, "Java": 70, "C++": 65},
    width=50,
    bar_styles=["blue", "yellow", "red", "green"],
)
panel = Panel(chart5, title="Programming Language Popularity", border_style="blue")
print(panel)

print("\n[bold]Example 6: Vertical Bar Chart[/bold]")
vertical = BarChart(
    {"Jan": 3, "Feb": 7, "Mar": 5, "Apr": 9},
    orientation="vertical",
    chart_height=8,
    bar_width=2,
    bar_styles=["cyan", "magenta", "yellow", "green"],
    label_style="bold",
)
print(vertical)
 
print("\n[bold]Example 7: Grouped Horizontal Bars[/bold]")
grouped_quarters = {
    "Q1": {"North": 32, "South": 28, "East": 25},
    "Q2": {"North": 38, "South": 30, "East": 29},
    "Q3": {"North": 34, "South": 35, "East": 30},
    "Q4": {"North": 40, "South": 37, "East": 33},
}
chart7 = BarChart(
    grouped_quarters,
    width=70,
    show_values=True,
    bar_width=2,
    group_styles=["red", "green", "cyan"],
    label_style="bold",
    value_style="dim",
)
print(chart7)

print("\n[bold]Example 8: Grouped Vertical Bars[/bold]")
chart8 = BarChart(
    grouped_quarters,
    orientation="vertical",
    chart_height=12,
    bar_width=2,
    group_gap=2,
    group_styles=["red", "green", "cyan"],
    label_style="bold",
)
print(chart8)