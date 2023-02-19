from datetime import date
from octanexchange.domain.currency import Currency
from octanexchange.domain.exchange_rate import ExchangeRatesWriter
from octanexchange.domain.repositories import BaseExchangesRepository
from typing import List


class HistoryUseCase:
    "Obtain a list of exchange rates from `exchange_repo` and write them using `exchange_writer`"
    def __init__(self, exchange_repo:BaseExchangesRepository, exchange_writer:ExchangeRatesWriter):
        self.exchange_repo = exchange_repo
        self.exchange_writer = exchange_writer

    def export_history(
        self, start_date:date, end_date:date, base:Currency, target_currencies:List[Currency]
    ):
        exchange_rates = (
            self.exchange_repo.get_history(start_date, end_date, base, target_currencies)
            if end_date >= start_date
            else []
        )

        self.exchange_writer.write(exchange_rates)
