from abc import abstractmethod
from datetime import date as date_type
import io
import json
from octanexchange.domain.exchange_rate import ExchangeRate, ExchangeRatesWriter
from typing import List


class SerializableExchangeRate:
    def __init__(self, exchange_rate:ExchangeRate):
        self.date = str(exchange_rate.date)
        self.base = exchange_rate.base.name
        self.symbol = exchange_rate.target.name
        self.rate = exchange_rate.rate


class JSONExchangeRateWriter(ExchangeRatesWriter):
    def convert_to_json_str(self, exchange_rates:List[ExchangeRate]):
        return "\n".join(json.dumps(vars(SerializableExchangeRate(ex_rate))) for ex_rate in exchange_rates)


class FileJSONExchangeRateWriter(JSONExchangeRateWriter):
    def __init__(self, out_path:str):
        self.out_path = out_path

    def write(self, exchange_rates:List[ExchangeRate]):
        "Write a list of currencies to a file"
        with open(self.out_path, 'w') as f:
            f.write(self.convert_to_json_str(exchange_rates))


class StdoutJSONExchangeRateWriter(JSONExchangeRateWriter):
    def write(self, exchange_rates:List[ExchangeRate]):
        print(self.convert_to_json_str(exchange_rates))
