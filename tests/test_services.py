from datetime import datetime

from src.services import investment_bank


def test_investment_bank(trans_for_services):
    date_obj = datetime(2021, 12, 31)
    str_date = datetime.strftime(date_obj, "%Y-%m")
    assert investment_bank(str_date, trans_for_services, 50) == "220500.0"
    date_obj = datetime(2021, 5, 31)
    str_date = datetime.strftime(date_obj, "%Y-%m")
    assert investment_bank(str_date, trans_for_services, 50) == 0