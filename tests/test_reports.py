import json

import pandas as pd

from src.reports import decorator_with_args, my_decorator, path_to_json, path_to_json_2, spending_by_weekday
from src.services import path_to_project


def test_my_decorator():
    @my_decorator
    def test_spending_by_weekday():
        path_to_file = path_to_project / "data" / "operations.xlsx"
        df_file = pd.read_excel(path_to_file)
        data = {
            "Wednesday": -753.68,
            "Tuesday": -549.29,
            "Monday": -1356.3,
            "Sunday": -1303.8,
            "Saturday": -311.52,
            "Friday": -2358.73,
            "Thursday": -435.24,
        }
        data = json.dumps(data)
        assert spending_by_weekday(df_file, date="14.10.2020") == data
        return spending_by_weekday(df_file, date="14.10.2020")

    result = test_spending_by_weekday()
    with open(path_to_json, encoding="utf-8") as file:
        data_json = json.load(file)
    assert result == data_json


def test_decorator_with_args():
    @decorator_with_args(path_to_json_2)
    def test_spending_by_weekday():
        path_to_file = path_to_project / "data" / "operations.xlsx"
        df_file = pd.read_excel(path_to_file)
        data = {
            "Wednesday": -753.68,
            "Tuesday": -549.29,
            "Monday": -1356.3,
            "Sunday": -1303.8,
            "Saturday": -311.52,
            "Friday": -2358.73,
            "Thursday": -435.24,
        }
        data = json.dumps(data)
        assert spending_by_weekday(df_file, date="14.10.2020") == data
        return spending_by_weekday(df_file, date="14.10.2020")

    result = test_spending_by_weekday()
    with open(path_to_json_2, encoding="utf-8") as file:
        data_json = json.load(file)
    assert result == data_json