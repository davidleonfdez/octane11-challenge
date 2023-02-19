from datetime import date
from octanexchange.domain.currency import Currency
from octanexchange.domain.exchange_rate import ExchangeRate, ExchangeRatesWriter
from octanexchange.domain.repositories import BaseExchangesRepository
from typing import List


cad = Currency("CAD")
eur = Currency("EUR")
usd = Currency("USD")


# Don't modify the amounts. Some tests rely on these values to do explicit checks
fake_exchanges = [
    ExchangeRate(date(2023, 2, 6), eur, usd, 1),
    ExchangeRate(date(2023, 2, 6), usd, eur, 1),
    ExchangeRate(date(2023, 2, 7), eur, usd, 2),
    ExchangeRate(date(2023, 2, 7), usd, eur, 0.5),
    ExchangeRate(date(2023, 2, 8), eur, usd, 1.5),
    ExchangeRate(date(2023, 2, 8), usd, eur, 1/1.5),
    ExchangeRate(date(2023, 2, 8), eur, cad, 1.7),
    ExchangeRate(date(2023, 2, 8), cad, eur, 1/1.7),
    ExchangeRate(date(2023, 2, 9), eur, usd, 0.4),
    ExchangeRate(date(2023, 2, 9), usd, eur, 2.5),
    ExchangeRate(date(2023, 2, 10), eur, usd, 1.1),
    ExchangeRate(date(2023, 2, 10), usd, eur, 1/1.1),
    ExchangeRate(date(2023, 2, 13), eur, usd, 0.6),
    ExchangeRate(date(2023, 2, 13), usd, eur, 1/0.6),
    ExchangeRate(date(2023, 2, 14), eur, usd, 1.3),
    ExchangeRate(date(2023, 2, 14), usd, eur, 1/1.3),
    ExchangeRate(date(2023, 2, 15), eur, usd, 1.4),
    ExchangeRate(date(2023, 2, 15), usd, eur, 1/1.4),
]


class FakeExchangesRepository(BaseExchangesRepository):
    def __init__(self, all_exchanges:List[ExchangeRate]=None):
        self.all_exchanges = all_exchanges if all_exchanges is not None else fake_exchanges

    def get_one(self, date:date, base:Currency, target_currency:Currency) -> ExchangeRate:
        def _is_wanted(exchange:ExchangeRate): 
            return (
                (exchange.date == date) 
                and (exchange.base == base) 
                and (exchange.target == target_currency)
            )

        return next((ex for ex in self.all_exchanges if _is_wanted(ex)), None)

    def get_history(
        self, start_date:date, end_date:date, base:Currency, target_currencies:List[Currency]
    ) -> List[ExchangeRate]:
        target_currencies_names = set(cur.name for cur in target_currencies)
        def _is_wanted(exchange:ExchangeRate): 
            return (
                (exchange.date >= start_date) 
                and (exchange.date <= end_date)
                and (exchange.base == base) 
                and (exchange.target.name in target_currencies_names)
            )

        return [ex for ex in self.all_exchanges if _is_wanted(ex)]


class DummyExchangeWriter(ExchangeRatesWriter):
    def __init__(self):
        self.n_calls = 0

    def write(self, exchange_rates:List[ExchangeRate]):
        self.exchange_rates = exchange_rates
        self.n_calls += 1
