from datetime import date
from octanexchange.domain.repositories import BaseCurrenciesRepository, BaseExchangesRepository
from octanexchange.domain.currency import Currency
from octanexchange.domain.exchange_rate import ExchangeRate
import requests
from typing import List


HTTP_NOT_FOUND_CODE = 404
RATES_KEY = "rates"


class FrankfurterHttpExchangesRepository(BaseExchangesRepository):
    def __init__(self, url:str):
        self.url = url

    def get_one(self, date:date, base:Currency, target_currency:Currency) -> ExchangeRate:
        url = f"{self.url}/{date}?from={base.name}&to={target_currency.name}"
        response = requests.get(url)
        if response.status_code == HTTP_NOT_FOUND_CODE:
            # The API returns HTTP not found when there are not rates for the range passed
            return None
        elif not response.ok:
            raise RuntimeError(f"Error in request to {url}")

        rate = response.json()[RATES_KEY][target_currency.name]

        return ExchangeRate(date, base, target_currency, rate)

    def get_history(
        self, start_date:date, end_date:date, base:Currency, target_currencies:List[Currency]
    ) -> List[ExchangeRate]:
        comma_sep_target_currency_names = ",".join(c.name for c in target_currencies)
        url = f"{self.url}/{start_date}..{end_date}?from={base.name}&to={comma_sep_target_currency_names}"
        try:
            response = requests.get(url)
            if response.status_code == HTTP_NOT_FOUND_CODE:
                # The API returns HTTP not found when there are no rates for the range passed
                return []
            elif not response.ok:
                raise RuntimeError(f"Error in request to {url}")

            response_dict = response.json()
            rates_dict:dict = response_dict[RATES_KEY]
            map(map, rates_dict.items())
            return [
                ExchangeRate(
                    date.fromisoformat(date_str),
                    Currency(base.name),
                    Currency(target_currency_symbol),
                    rate,
                )
                for date_str, rates_by_target_currency in rates_dict.items()
                for target_currency_symbol, rate in rates_by_target_currency.items()
            ]
        except:
            # Some strange ValueError happens in urllib when the response is empty.
            # TODO: we should ideally log the specific error
            return []


class FrankfurterHttpCurrenciesRepository(BaseCurrenciesRepository):
    CURRENCIES_ENDPOINT = "currencies"

    def __init__(self, url:str):
        self.url = url

    def get_all(self) -> List[Currency]:
        url = f"{self.url}/{self.CURRENCIES_ENDPOINT}"
        response = requests.get(url)

        if not response.ok:
            raise RuntimeError(f"Error in request to {url}")

        currencies_dict = response.json()
        return map(Currency, currencies_dict.keys())
