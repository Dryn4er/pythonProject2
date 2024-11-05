from src.reports import df_file, spending_by_weekday, str_date_report
from src.services import bank_investments, str_date_service, transactions
from src.utils import currency, greeting, get_card_number, read_file, stock_prices, write_to_file, top_transactions
from src.views import main, str_begin_date

if __name__ == "__main__":
    print(
        write_to_file(
            stock_prices(
                currency(
                    top_transactions(
                        read_file(main(str_begin_date)), get_card_number(read_file(main(str_begin_date)), greeting())
                    )
                )
            )
        )
    )

    print(bank_investments(str_date_service, transactions, 50))

    print(spending_by_weekday(df_file, str_date_report))