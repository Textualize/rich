"""
Builds calendar layout using Columns and Tables.
Usage:
python calendar_layout.py [YEAR]
Example:
python calendar_layout.py 2021
"""
import argparse

import calendar
from datetime import datetime

from rich.table import Table
from rich.columns import Columns
from rich import print


def display_calendar(year):

    today = datetime.today()
    year = int(year)
    cal = calendar.Calendar()

    tables = []
    for month in range(1, 13):

        table = Table(title=f"{calendar.month_name[month]} {year}", style="green")

        for week_day in cal.iterweekdays():
            table.add_column("{:.3}".format(calendar.day_name[week_day]))

        month_days = cal.monthdayscalendar(year, month)
        for weekdays in month_days:
            days = []
            for day in weekdays:
                today_tuple = today.day, today.month, today.year

                if day and (day, month, year) == today_tuple:
                    _day = f"[bold underline red]{day}"
                else:
                    _day = "" if day == 0 else str(day)
                days.append(_day)
            table.add_row(*days)

        tables.append(table)

    columns = Columns(tables, equal=True, expand=True)
    print(columns)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rich calendar")
    parser.add_argument("year", metavar="year", type=int)
    args = parser.parse_args()

    display_calendar(args.year)
