from abc import ABC, abstractmethod
from .currency import Currency
from dataclasses import dataclass
from datetime import date
from typing import List


@dataclass(eq=True, frozen=True)
class ExchangeRate:
    date:date
    base:Currency
    target:Currency
    rate:float


class ExchangeRatesWriter(ABC):
    @abstractmethod
    def write(self, exchange_rates:List[ExchangeRate]):
        "Writes a list of exchange rates to some destination"
