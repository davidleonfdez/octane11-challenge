from octanexchange.config import Config
from octanexchange.domain.repositories import BaseCurrenciesRepository, BaseExchangesRepository
from octanexchange.infrastructure.exchange_rate_io import (
    ExchangeRatesWriter, FileJSONExchangeRateWriter, StdoutJSONExchangeRateWriter
)
from octanexchange.infrastructure.frankfurter_http_repositories import (
    FrankfurterHttpCurrenciesRepository, FrankfurterHttpExchangesRepository
)


class Dependencies():
    "Dependencies resolver. Instances are cached for non-parameterized properties."
    def __init__(self, config:Config):
        self.config = config
        self._currencies_repo = None
        self._exchanges_repo = None

    @property
    def currencies_repo(self) -> BaseCurrenciesRepository:
        if self._currencies_repo is None:
            self._currencies_repo = FrankfurterHttpCurrenciesRepository(self.config.exchanges_api_url)
        return self._currencies_repo

    @property
    def exchange_rates_repo(self) -> BaseExchangesRepository:
        if self._exchanges_repo is None:
            self._exchanges_repo = FrankfurterHttpExchangesRepository(self.config.exchanges_api_url)
        return self._exchanges_repo

    def exchange_rates_writer(self, output_path:str) -> ExchangeRatesWriter:
        output_path = output_path.strip()
        return FileJSONExchangeRateWriter(output_path) if len(output_path) > 0 else StdoutJSONExchangeRateWriter()
