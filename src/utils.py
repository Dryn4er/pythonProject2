import json
import logging

# import os
from datetime import datetime
from pathlib import Path

from pandas import Timestamp

# import openpyxl
# import requests
# from dotenv import load_dotenv

path_to_project = Path(__file__).resolve().parent.parent
path_to_file = path_to_project / "data" / "operations.xlsx"

logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)
fileHandler = logging.FileHandler(path_to_project / "logs" / "utils.log", encoding="UTF-8", mode="w")
fileFormatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
fileHandler.setFormatter(fileFormatter)
logger.addHandler(fileHandler)


def read_file(file):
    """Читаем DataFrame, возвращаем список словарей"""
    transactions = []
    # headers = file.columns.tolist()
    file["Номер карты"] = file["Номер карты"].fillna(False)
    try:
        logger.info("We have an adequate list of dictionaries")
        for index, row in file.iterrows():
            row_data = row.to_dict()
            if row_data["Номер карты"]:
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
            if len(transactions) == 100:
                break
            else:
                continue
        return transactions
    except Exception as e:
        logger.error("What do you want, bitch?!")
        print(f"We have a problem with a reading file, Watson: {e}")


def greeting():
    """Приветствуем пользователя в зависимости от времени суток, возвращаем словарь info с приветствием"""
    try:
        logger.info("Say 'hello'")
        date = datetime.now()
        str_date = date.strftime("%Y-%m-%d %H:%M:%S")
        hour = str_date[11:13]
        info = {}
        if 4 <= int(hour) < 12:
            info["greeting"] = "Доброе утро"
            return info
        elif 12 <= int(hour) < 18:
            info["greeting"] = "Добрый день"
            return info
        elif 18 <= int(hour) < 22:
            info["greeting"] = "Добрый вечер"
            return info
        else:
            info["greeting"] = "Доброй ночи"
        return info
    except Exception as e:
        logger.error("You can`t say hello, bitch?!")
        print(f"We have a problem with a reading file, Watson: {e}")


def number_cards(trans, info):
    """Получаем последние 4 цифры номера карты, добавляем в словарь info, возвращаем его же"""
    try:
        logger.info("Get numbers of cards ")
        info["cards"] = []
        for transaction in trans:
            card_number = transaction.get("Номер карты")
            if card_number is not None:
                card_number_str = str(card_number)
                if len(card_number_str) > 1:
                    last_digits = transaction.get("Номер карты")[1:]
                    if not any(card["last_digits"] == last_digits for card in info["cards"]):
                        info["cards"].append({"last_digits": last_digits, "total_spent": 0, "cashback": 0})
                    for card in info["cards"]:
                        if card["last_digits"] == last_digits:
                            if "-" in str(transaction["Сумма платежа"]):
                                amount = str(transaction["Сумма платежа"])[1:]
                                cash_back = float(amount) / 100
                            else:
                                continue
                            card["total_spent"] += float(amount)
                            card["cashback"] += cash_back
        return info
    except Exception as e:
        logger.error("Fucking numbers of cards")
        print(f"We have a problem with getting of numbers card, Watson: {e}")


def top_transactions(trans, info):
    """Получаем отсортированные транзакции по убыванию, добавляем в словарь info"""
    try:
        logger.info("Oh, you are so rich...")
        top = sorted(trans, key=lambda x: x["Сумма операции"])[:5]
        info["top_transactions"] = []
        for trans in top:
            info["top_transactions"].append(
                {
                    "date": trans["Дата платежа"],
                    "amount": trans["Сумма операции"],
                    "category": trans["Категория"],
                    "description": trans["Описание"],
                }
            )
        return info
    except Exception as e:
        logger.error("You poor fuck...")
        print(f"We have a problem with top transactions, Watson: {e}")


def currency(info):
    """Подключаемся к API, получаем курсы валют USD и EUR в отношении рубля, добавляем в словарь info"""
    try:
        logger.info("Where do you have so much currency from?")
        # load_dotenv()
        # access_key_curr = os.getenv("access_key_curr")
        #
        # headers_curr = {"apikey": access_key_curr}
        # url_usd = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base=USD"
        #
        # result_usd = requests.get(url_usd, headers=headers_curr)
        # new_amount_usd = result_usd.json()
        #
        # url_eur = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base=EUR"
        # result_eur = requests.get(url_eur, headers=headers_curr)
        # new_amount_eur = result_eur.json()

        info["currency_rates"] = []

        #     info['currency_rates'].append({
        #   "currency": "USD",
        #   "rate": new_amount_usd['rates']['RUB']
        # })
        #
        #     info['currency_rates'].append({
        #         "currency": "EUR",
        #         "rate": new_amount_eur['rates']['RUB']
        #     })

        info["currency_rates"].append({"currency": "USD", "rate": 95.676332})
        info["currency_rates"].append({"currency": "EUR", "rate": 104.753149})
        return info
    except Exception as e:
        logger.error("Everybody has problems with currency now...")
        print(f"We have a problem with currency, Watson: {e}")


def stock_prices(info):
    """Подключаемся к API, получаем наименование акции и ее цену, добавляем в словарь info"""
    try:
        logger.info("Good stocks")
        # load_dotenv()
        # access_key_stock = os.getenv("access_key_stock")
        # conn = http.client.HTTPSConnection("real-time-finance-data.p.rapidapi.com")
        #
        # headers = {
        #     "x-rapidapi-key": access_key_stock,
        #     "x-rapidapi-host": "real-time-finance-data.p.rapidapi.com",
        # }
        #
        # conn.request("GET", "/market-trends?trend_type=MARKET_INDEXES&country=us&language=en", headers=headers)
        #
        # res = conn.getresponse()
        # data = res.read()
        # data_json = json.loads(data.decode("utf-8"))
        data_json = {
            "data": {
                "trends": [
                    {"name": "S&P 500", "price": 4500.50},
                    {"name": "Dow Jones", "price": 34000.75},
                    {"name": "NASDAQ", "price": 15000.25},
                ]
            }
        }

        info["stock_prices"] = []

        for trend in data_json["data"]["trends"]:
            info["stock_prices"].append({"stock": trend["name"], "price": trend["price"]})
        return info
    except Exception as e:
        logger.error("Everybody has problems with foreign stocks.")
        print(f"We have a problem with stocks, Watson: {e}")


def to_file(info):
    """Записываем словарь info в json файл, возвращаем словарь info в PYTHON виде"""
    try:
        logger.info("Write to file")
        if info is None:
            logger.error("Info is None")
            return

        info_to_file = {}
        info_to_file["user_currencies"] = []
        info_to_file["user_stocks"] = []

        if "currency_rates" in info:
            for currency_info in info["currency_rates"]:
                info_to_file["user_currencies"].append(currency_info["currency"])

        if "stock_prices" in info:
            for stock_info in info["stock_prices"]:
                info_to_file["user_stocks"].append(stock_info["stock"])

        path_to_project = Path(__file__).resolve().parent.parent
        path_to_file = path_to_project / "user_settings.json"
        with open(path_to_file, "w", encoding="UTF-8") as f:
            json.dump(info_to_file, f, ensure_ascii=False)

        for key, value in info.items():
            if isinstance(value, list):
                for item in value:
                    for k, v in item.items():
                        if isinstance(v, Timestamp):
                            item[k] = v.isoformat()

        json_info = json.dumps(info, ensure_ascii=False)

        return json_info
    except Exception as e:
        logger.error("Problems with recording to file.")
        print(f"We have a problem with recording to file, Watson: {e}")