from datetime import datetime, timedelta

import pandas as pd

from src.utils import (
    currency,
    greeting,
    number_cards,
    path_to_file,
    read_file,
    stock_prices,
    to_file,
    top_transactions,
)

begin_date = datetime(2020, 5, 25, 15, 46, 57)
str_begin_date = datetime.strftime(begin_date, "%Y-%m-%d %H:%M:%S")


def get_operations() -> pd.DataFrame:
    """Читаем файл Excel"""
    df = pd.read_excel(path_to_file)

    datetime_fields_to_convert = {
        "Дата операции": "%d.%m.%Y %H:%M:%S",
        "Дата платежа": "%d.%m.%Y",
    }
    for datetime_field, str_format in datetime_fields_to_convert.items():
        df[datetime_field] = pd.to_datetime(df[datetime_field], format=str_format)

    return df


def filter_operations_by_date(df: pd.DataFrame, date: str):
    """Фильтрация транзакций по дате"""
    dt = datetime.strptime(date, "%d-%m-%Y %H:%M:%S")
    start_date = pd.to_datetime(dt.replace(day=1))
    end_date = pd.to_datetime(dt + timedelta(days=1))
    return df.loc[(df["Дата операции"] >= start_date) & (df["Дата операции"] < end_date)]


def main(analysis_date):
    """Получаем транзакции из Excel файла, фильтрованные по дате"""
    object_date = datetime.strptime(analysis_date, "%Y-%m-%d %H:%M:%S")
    new_analysis_date = datetime.strftime(object_date, "%d-%m-%Y %H:%M:%S")
    df = get_operations()
    df = filter_operations_by_date(df, new_analysis_date)
    return df


if __name__ == "__main__":
    print(
        to_file(
            stock_prices(
                currency(
                    top_transactions(
                        read_file(main(str_begin_date)), number_cards(read_file(main(str_begin_date)), greeting())
                    )
                )
            )
        )
    )