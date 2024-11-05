import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import openpyxl

path_to_project = Path(__file__).resolve().parent.parent
path_to_file = path_to_project / "data" / "operations.xlsx"

logger = logging.getLogger("services")
logger.setLevel(logging.DEBUG)
fileHandler = logging.FileHandler(path_to_project / "logs" / "services.log", encoding="UTF-8", mode="w")
fileFormatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
fileHandler.setFormatter(fileFormatter)
logger.addHandler(fileHandler)


date_obj = datetime(2021, 5, 31)
str_date_service = datetime.strftime(date_obj, "%Y-%m")


workbook = openpyxl.load_workbook(path_to_file)
sheet = workbook.active
headers = [cell.value for cell in sheet[1]]
transactions = []
try:
    logger.info("Создали список словарей")
    for row in sheet.iter_rows(min_row=2, values_only=True):
        row_data = dict(zip(headers, row))
        transactions.append(
            {
                "Дата операции": row_data["Дата операции"],
                "Дата платежа": row_data["Дата платежа"],
                "Номер карты": row_data["Номер карты"],
                "Статус": row_data["Статус"],
                "Сумма операции": row_data["Сумма операции"],
                "Валюта операции": row_data["Валюта операции"],
                "Сумма платежа": row_data["Сумма платежа"],
                "Валюта платежа": row_data["Валюта платежа"],
                "Кэшбэк": row_data["Кэшбэк"],
                "Категория": row_data["Категория"],
                "MCC": row_data["MCC"],
                "Описание": row_data["Описание"],
                "Бонусы (включая кэшбэк)": row_data["Бонусы (включая кэшбэк)"],
                "Округление на инвесткопилку": row_data["Округление на инвесткопилку"],
                "Сумма операции с округлением": row_data["Сумма операции с округлением"],
            }
        )
        if len(transactions) == 1500:
            break
except Exception as e:
    logger.error(f"Ошибка с созданием списка словарей: {e}.")
    print(f"Ошибка с созданием списка словарей: {e}.")


def bank_investments(month: str, list_transactions: List[Dict[str, Any]], limit: int):
    """На вход принимаем месяц, транзакции, кратная сумма, до которой округляем.
    Каждая покупка округляется до кратной суммы
    и падает в counter"""
    try:
        logger.info("Общая сумма")
        counter = 0
        for i in list_transactions:
            if i["Дата платежа"] is None:
                counter += 0
                continue
            date = datetime.strptime(i["Дата платежа"], "%d.%m.%Y")
            need_data = datetime.strftime(date, "%Y-%m")
            obj_date = datetime.strptime(need_data, "%Y-%m")
            obj_month = datetime.strptime(month, "%Y-%m")
            if obj_date == obj_month:
                for dictionary in list_transactions:
                    payment = dictionary["Сумма платежа"]
                    if payment < 0:
                        investment = round((int(payment)) // limit) * limit
                        counter += investment
                    else:
                        counter += 0
                        continue
            else:
                counter += 0
                continue
        if counter == 0:
            return counter
        counter = str(counter)[1:]
        json_counter = json.dumps(float(counter), ensure_ascii=False)
        return json_counter
    except Exception as e:
        logger.error(f"Нет сэкономленных средств: {e}.")
        print(f"Нет сэкономленных средств: {e}.")


if __name__ == "__main__":
    print(bank_investments(str_date_service, transactions, 50))