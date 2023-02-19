# Octane11-challenge

Octane11 code challenge

## Installation

`pip install .`

## Run all tests

`python -m pytest tests`

## Usage examples:

### Export

Print the daily exchange rates between 2021-02-01 and 2021-02-02 from USD to EUR and USD to CAD:

`python exrates.py --start 2021-02-01 --end 2021-02-02 --base USD --symbol EUR CAD`

Output:

```
{"date": "2021-02-01", "base": "USD", "symbol": "CAD", "rate": 1.2805}
{"date": "2021-02-01", "base": "USD", "symbol": "EUR", "rate": 0.82754}
{"date": "2021-02-02", "base": "USD", "symbol": "CAD", "rate": 1.2805}
{"date": "2021-02-02", "base": "USD", "symbol": "EUR", "rate": 0.83029}
```

To export to a file:

```
python src/octanexchange/exrates.py history --start 2021-02-01 --end 2021-02-02 --base USD --symbol EUR CAD --output rates.jsonl
cat rates.jsonl
```

... and we get the same output.

### Convert

Convert 50 USD to EUR according to the rate valid at 2021-02-01:

`python src/octanexchange/exrates.py convert --date 2021-02-01 --base USD --symbol EUR --amount 50`

The output is:

`41.377`


## Potential improvements

- Add a logger
- Return complex object from use cases that includes an error code or flag
- Think about float precision, it could matter
    - Use value object for rate
- `Dependency` class should ideally be replaced by a dependency injector.
