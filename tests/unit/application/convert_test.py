from datetime import date
import math
from fakes import cad, eur, usd, FakeExchangesRepository
from octanexchange.application.convert import ConvertUseCase
from octanexchange.domain.currency import Currency
from octanexchange.domain.exchange_rate import ExchangeRate
import pytest


exchanges_repo = FakeExchangesRepository()


def test_regular_day():
    use_case = ConvertUseCase(exchanges_repo)
    ex_date = date(2023, 2, 7)
    in_amount = 5.5

    actual_amount_usd = use_case.convert(ex_date, eur, usd, in_amount)
    actual_amount_eur = use_case.convert(ex_date, usd, eur, actual_amount_usd)
    expected_rate_eur_to_usd = 2
    expected_amount_usd = expected_rate_eur_to_usd * in_amount
    # We are assuming that the test rates are coherent, so eur -> usd -> eur returns
    # the initial amount
    expected_amount_eur = in_amount

    assert math.isclose(actual_amount_usd, expected_amount_usd)
    assert math.isclose(actual_amount_eur, expected_amount_eur)


def test_missing():
    use_case = ConvertUseCase(exchanges_repo)
    ex_date = date(2022, 2, 7)

    with pytest.raises(RuntimeError):
        use_case.convert(ex_date, eur, usd, 100)


def test_weekend():
    use_case = ConvertUseCase(exchanges_repo)
    a_sunday = date(2023, 2, 12)
    in_amount = 45
    previous_friday_rate = 1.1

    actual_amount = use_case.convert(a_sunday, eur, usd, in_amount)
    expected_amount = previous_friday_rate * in_amount

    assert math.isclose(actual_amount, expected_amount)
