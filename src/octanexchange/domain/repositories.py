from abc import ABC, abstractmethod
from datetime import date
from octanexchange.domain.currency import Currency
from octanexchange.domain.exchange_rate import ExchangeRate
from typing import List


class BaseExchangesRepository(ABC):
    @abstractmethod
    def get_one(self, date:date, base:Currency, target_currency:Currency) -> ExchangeRate:
        pass

    @abstractmethod
    def get_history(
        self, start_date:date, end_date:date, base:Currency, target_currencies:List[Currency]
    ) -> List[ExchangeRate]:
        pass


class BaseCurrenciesRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Currency]:
        pass
