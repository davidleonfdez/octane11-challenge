from datetime import date, timedelta
from fakes import cad, eur, usd, DummyExchangeWriter, FakeExchangesRepository, fake_exchanges
from octanexchange.application.history import HistoryUseCase


def test_zero_days():
    writer = DummyExchangeWriter()
    use_case = HistoryUseCase(
        FakeExchangesRepository(),
        writer,
    )
    start_date = date(2023, 2, 8)
    end_date = start_date - timedelta(days=1)

    use_case.export_history(start_date, end_date, eur, [usd])
    actual_ex_rates = writer.exchange_rates

    assert len(actual_ex_rates) == 0


def test_one_day():
    writer = DummyExchangeWriter()
    use_case = HistoryUseCase(
        FakeExchangesRepository(),
        writer,
    )
    start_date = date(2023, 2, 8)
    base = eur
    target_currencies = [cad, usd]

    use_case.export_history(start_date, start_date, base, target_currencies)
    expected_ex_rates = [
        ex 
        for ex in fake_exchanges 
        if (ex.date == start_date) and (ex.base == base) and (ex.target in target_currencies)
    ]

    assert set(writer.exchange_rates) == set(expected_ex_rates)
    assert writer.n_calls == 1

def test_multiple_days():
    writer = DummyExchangeWriter()
    use_case = HistoryUseCase(
        FakeExchangesRepository(),
        writer,
    )
    start_date = date(2023, 2, 8)
    end_date = date(2023, 2, 14)
    base = usd
    target_currencies = [eur]

    use_case.export_history(start_date, end_date, base, target_currencies)
    expected_ex_rates = [
        ex 
        for ex in fake_exchanges 
        if (ex.date >= start_date) and (ex.date <= end_date) and (ex.base == base) and (ex.target in target_currencies)
    ]

    assert set(writer.exchange_rates) == set(expected_ex_rates)
    assert writer.n_calls == 1

