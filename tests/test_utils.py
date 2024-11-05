import json
import unittest
from datetime import datetime
from unittest.mock import patch

import pandas as pd
import pytest

from src.utils import currency, greeting, number_cards, read_file, stock_prices, to_file, top_transactions


class TestReadFile(unittest.TestCase):
    @patch("logging.getLogger")
    def test_read_file(self, mock_logger):
        data = {
            "Дата операции": ["2023-01-01", "2023-01-02"],
            "Дата платежа": ["2023-01-01", "2023-01-02"],
            "Номер карты": ["1234", "5678"],
            "Статус": ["завершен", "отменен"],
            "Сумма операции": [100.00, 150.00],
            "Валюта операции": ["RUB", "RUB"],
            "Сумма платежа": [100.00, 150.00],
            "Валюта платежа": ["RUB", "RUB"],
            "Кэшбэк": [1.00, 1.50],
            "Категория": ["продукты", "развлечения"],
            "MCC": [5411, 5813],
            "Описание": ["магазин", "кинотеатр"],
            "Бонусы (включая кэшбэк)": [10.00, 15.00],
            "Округление на инвесткопилку": [0.00, 0.00],
            "Сумма операции с округлением": [100.00, 150.00],
        }

        file = pd.DataFrame(data)

        transactions = read_file(file)

        expected_transactions = [
            {
                "Дата операции": "2023-01-01",
                "Дата платежа": "2023-01-01",
                "Номер карты": "1234",
                "Статус": "завершен",
                "Сумма операции": 100.00,
                "Валюта операции": "RUB",
                "Сумма платежа": 100.00,
                "Валюта платежа": "RUB",
                "Кэшбэк": 1.00,
                "Категория": "продукты",
                "MCC": 5411,
                "Описание": "магазин",
                "Бонусы (включая кэшбэк)": 10.00,
                "Округление на инвесткопилку": 0.00,
                "Сумма операции с округлением": 100.00,
            },
            {
                "Дата операции": "2023-01-02",
                "Дата платежа": "2023-01-02",
                "Номер карты": "5678",
                "Статус": "отменен",
                "Сумма операции": 150.00,
                "Валюта операции": "RUB",
                "Сумма платежа": 150.00,
                "Валюта платежа": "RUB",
                "Кэшбэк": 1.50,
                "Категория": "развлечения",
                "MCC": 5813,
                "Описание": "кинотеатр",
                "Бонусы (включая кэшбэк)": 15.00,
                "Округление на инвесткопилку": 0.00,
                "Сумма операции с округлением": 150.00,
            },
        ]

        self.assertEqual(transactions, expected_transactions)


@pytest.mark.parametrize(
    ("now_datetime", "expected_greeting"),
    [
        (datetime(2024, 1, 1, hour=6, minute=0), {"greeting": "Доброе утро"}),
        (datetime(2024, 1, 1, hour=14, minute=0), {"greeting": "Добрый день"}),
        (datetime(2024, 1, 1, hour=20, minute=0), {"greeting": "Добрый вечер"}),
        (datetime(2024, 1, 1, hour=23, minute=0), {"greeting": "Доброй ночи"}),
    ],
)
@patch("src.utils.datetime")
def test_get_greeting(mocked_datetime, now_datetime, expected_greeting):
    mocked_datetime.now.return_value = now_datetime
    assert greeting() == expected_greeting


def test_number_cards(trans):
    assert number_cards(trans, {}) == {"cards": [{"last_digits": "7197", "total_spent": 131.6, "cashback": 1.316}]}


def test_top_transactions(trans):
    assert top_transactions(trans, {}) == {
        "top_transactions": [
            {"date": "2020-05-28 00:00:00", "amount": -86.6, "category": "Супермаркеты", "description": "Магнит"},
            {"date": "2020-05-28 00:00:00", "amount": -45.0, "category": "Супермаркеты", "description": "Колхоз"},
        ]
    }


@pytest.mark.parametrize(
    "info, exit_currency",
    [({}, {"currency_rates": [{"currency": "USD", "rate": 95.676332}, {"currency": "EUR", "rate": 104.753149}]})],
)
def test_currency(info, exit_currency):
    assert currency(info) == exit_currency


@pytest.mark.parametrize(
    "input_stock, exit_stock",
    [
        (
            {},
            {
                "stock_prices": [
                    {"stock": "S&P 500", "price": 4500.5},
                    {"stock": "Dow Jones", "price": 34000.75},
                    {"stock": "NASDAQ", "price": 15000.25},
                ]
            },
        )
    ],
)
def test_stock_prices(input_stock, exit_stock):
    assert stock_prices(input_stock) == exit_stock


def test_to_file(input_to_file, return_to_file):
    assert to_file(input_to_file) == json.dumps(return_to_file, ensure_ascii=False)