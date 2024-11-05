from unittest.mock import patch

import pandas as pd

from src.views import filter_operations_by_date, get_operations


@patch("src.views.pd.read_excel")
def test_get_operations(mock_excel):
    data = [
        {
            "Дата операции": "26.05.2020 13:29:09",
            "Дата платежа": "28.05.2020",
            "Номер карты": "*7197",
            "Сумма операции": -45.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -45.0,
            "Валюта платежа": "RUB",
        },
        {
            "Дата операции": "26.05.2020 13:23:32",
            "Дата платежа": "28.05.2020",
            "Номер карты": "*7197",
            "Сумма операции": -86.6,
            "Валюта операции": "RUB",
            "Сумма платежа": -86.6,
            "Валюта платежа": "RUB",
        },
    ]

    mock_excel.return_value = pd.DataFrame(data)
    result = get_operations()

    pd.testing.assert_frame_equal(result, mock_excel.return_value)


def test_filter_operations_by_date():
    initial_data = [
        pd.Timestamp("2024-09-01 10:00:00"),
        pd.Timestamp("2024-10-01 10:00:00"),
        pd.Timestamp("2024-10-02 10:00:00"),
        pd.Timestamp("2024-10-03 10:00:00"),
    ]
    df = pd.DataFrame({"Дата операции": initial_data})

    filtered_df = filter_operations_by_date(df, "02-10-2024 00:00:00")

    expected_data = [
        pd.Timestamp("2024-10-01 10:00:00"),
        pd.Timestamp("2024-10-02 10:00:00"),
    ]
    expected_df = pd.DataFrame({"Дата операции": expected_data})
    pd.testing.assert_frame_equal(filtered_df.reset_index(drop=True), expected_df.reset_index(drop=True))