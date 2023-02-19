import argparse
import datetime
from octanexchange.config import Config
from octanexchange.dependencies import Dependencies
from octanexchange.domain.currency import Currency
from octanexchange.application.convert import ConvertUseCase
from octanexchange.application.history import HistoryUseCase


HISTORY_CMD = "history"
CONVERT_CMD = "convert"
COMMAND_ATTR = "command"


def parse_args(config:Config, deps:Dependencies):
    parser = argparse.ArgumentParser(description="Historical exchange rates tool")
    # `dest` may be required for old Python versions to avoid a crash when we exec `python exrates.py` (w/o command)
    # See https://bugs.python.org/issue29298
    subparsers = parser.add_subparsers(help='Commands', required=True, dest=COMMAND_ATTR)

    valid_currency_names = [cur.name for cur in deps.currencies_repo.get_all()]
    if len(valid_currency_names) == 0:
        raise RuntimeError("Received an empty set of valid currency names from external service")
    
    default_currency = config.default_currency
    if default_currency not in valid_currency_names:
        default_currency = valid_currency_names[0]
        
    history_parser = subparsers.add_parser(
        HISTORY_CMD, 
        help="Export daily exchange rates between a date range; by default to std output, to a file if the param "
            "`output` is provided. Each line in the output has JSON format."
    )
    history_parser.add_argument(
        '--start', 
        type=datetime.date.fromisoformat, 
        default=datetime.date.today(), 
        help='Start date in ISO format. Default is today.',
    )
    history_parser.add_argument(
        '--end', 
        type=datetime.date.fromisoformat, 
        default=datetime.date.today(), 
        help='End date in ISO format, included in range. Default is today.',
    )
    history_parser.add_argument(
        '--base', 
        type=str, 
        default=default_currency, 
        help=f"Base currency. Default is {default_currency}.",
        choices=valid_currency_names,
    )
    history_parser.add_argument(
        '--symbol',
        help="List of currency symbols to convert to (space separated). Required.",
        required=True,
        nargs="+",
        choices=valid_currency_names,
    )
    history_parser.add_argument(
        '--output', 
        type=str, 
        default='', 
        help=(
            "File name to write the output to. If this flag is not specified, the result will be sent to std output "
            "instead."
        ),
    )

    convert_parser = subparsers.add_parser(CONVERT_CMD, help="Convert between currencies.")
    convert_parser.add_argument(
        '--date', 
        type=datetime.date.fromisoformat, 
        default=datetime.date.today(), 
        help='Currency exchange date in ISO format. Default is today.',
    )
    convert_parser.add_argument(
        '--base', 
        type=str, 
        default=default_currency, 
        help=f"Base currency. Default is {default_currency}.",
        choices=valid_currency_names
    )
    convert_parser.add_argument(
        '--symbol', help="Currency symbol to convert to. Required.", required=True, choices=valid_currency_names
    )
    convert_parser.add_argument('--amount', type=float, help="Amount to convert. Required.", required=True)

    args = parser.parse_args()
    return args


def check_parsed_values(args, parser:argparse.ArgumentParser):
    "Extra argument checks that can't be easily done by `argparse`"
    if args.command == HISTORY_CMD:
        if args.end < args.start:
            parser.error("'end' should be greater or equal than 'start'")
    #elif args.command == CONVERT_CMD:
        # extra convert checks should go here


def export_history(args, dependencies:Dependencies):
    use_case = HistoryUseCase(
        dependencies.exchange_rates_repo,
        dependencies.exchange_rates_writer(args.output),
    )
    use_case.export_history(
        args.start, 
        args.end, 
        Currency(args.base), 
        map(Currency, args.symbol),
    )


def convert(args, dependencies:Dependencies):
    use_case = ConvertUseCase(dependencies.exchange_rates_repo)
    converted_amount = use_case.convert(args.date, Currency(args.base), Currency(args.symbol), args.amount)
    print(converted_amount)


def main():
    config = Config()
    deps = Dependencies(config)

    args = parse_args(config, deps)

    actions = {
        HISTORY_CMD: export_history,
        CONVERT_CMD: convert,
    }
    actions[getattr(args, COMMAND_ATTR)](args, deps)


if __name__ == '__main__':
    main()
