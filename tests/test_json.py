import datetime

from rich.json import JSON


def test_print_json_data_with_default():
    date = datetime.date(2021, 1, 1)
    json = JSON.from_data({"date": date}, default=lambda d: d.isoformat())
    assert str(json.text) == '{\n  "date": "2021-01-01"\n}'
