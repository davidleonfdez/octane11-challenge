from datetime import date, timedelta
from octanexchange.domain.currency import Currency
from octanexchange.domain.exchange_rate import ExchangeRatesWriter
from octanexchange.domain.repositories import BaseExchangesRepository


class ConvertUseCase:
    "Convert an amount between currencies"
    def __init__(self, exchanges_repo:BaseExchangesRepository):
        self.exchanges_repo = exchanges_repo

    def convert(self, date:date, base:Currency, target:Currency, amount:float) -> float:
        if base == target:
            return amount

        # TODO: what if a day is missing???
        # -If it's missing because of weekend, we get the rates from the previous Friday
        queried_date = date
        friday_isoweekday = 5
        is_weekend = queried_date.isoweekday() > friday_isoweekday
        if is_weekend:
            # Go back to previous Friday
            queried_date = queried_date - timedelta(days=queried_date.isoweekday() - friday_isoweekday)
        exchange_rate = self.exchanges_repo.get_one(queried_date, base, target)

        if exchange_rate is None:
            raise RuntimeError(f"Exchange rate not available for {date}")

        return amount * exchange_rate.rate
