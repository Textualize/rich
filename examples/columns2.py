"""
Builds calendar layout using Columns and Tables.
Usage:
python columns2.py [YEAR]
Example:
python columns2.py 2021
"""
import argparse

import calendar
from datetime import datetime

from rich.table import Table
from rich.columns import Columns
from rich import print


def display_calendar(year=None):
    
    today = datetime.today()
    year = int(year or today.year)
    cal = calendar.Calendar()

    tables = []
    for month in range(1,13):

        table = Table(title=f"""{calendar.month_name[month]} {year}""", style="green")

        for wd in cal.iterweekdays():
            table.add_column("{:.3}".format(calendar.day_name[wd]))

        month_days = cal.monthdayscalendar(year, month)
        for weekdays in month_days:
            days = []
            for day in weekdays:
                today_tuple = today.day, today.month, today.year
                
                if day and (day, month, year) == today_tuple :
                    _day = "[bold underline red]%s[/]" % day   
                else:
                    _day = "%s" % ('' if day == 0 else day) 
                days.append(_day)
            table.add_row(*days)

        tables.append(table)

    columns = Columns(tables, equal=True, expand=True)
    print(columns)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Rich calendar')
    parser.add_argument('year', metavar='year', type=int, default=None)
    args = parser.parse_args()

    display_calendar(args.year)
