"""Command-line interface for the Upbit order system."""

from __future__ import annotations

import argparse
import json
from typing import Any

from upbit_order.config import load_env_file, load_settings
from upbit_order.system import UpbitOrderSystem


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Upbit order execution CLI")
    parser.add_argument("--env-file", default=".env", help="Path to a local env file.")

    commands = parser.add_subparsers(dest="command", required=True)

    markets = commands.add_parser("markets", help="List market tickers.")
    markets.add_argument("--fiat", default="KRW")

    price = commands.add_parser("price", help="Read current market price.")
    price.add_argument("markets", nargs="*", help="Markets such as KRW-BTC KRW-ETH.")

    candles = commands.add_parser("candles", help="Read OHLCV candles.")
    candles.add_argument("--market", default=None)
    candles.add_argument("--interval", default="minute1")
    candles.add_argument("--count", type=int, default=20)

    commands.add_parser("balances", help="Read account balances.")

    buy_limit = commands.add_parser("buy-limit", help="Place or simulate a limit buy.")
    buy_limit.add_argument("market")
    buy_limit.add_argument("price", type=float)
    buy_limit.add_argument("volume", type=float)
    buy_limit.add_argument("--execute", action="store_true")

    sell_limit = commands.add_parser("sell-limit", help="Place or simulate a limit sell.")
    sell_limit.add_argument("market")
    sell_limit.add_argument("price", type=float)
    sell_limit.add_argument("volume", type=float)
    sell_limit.add_argument("--execute", action="store_true")

    buy_market = commands.add_parser("buy-market", help="Place or simulate a market buy.")
    buy_market.add_argument("market")
    buy_market.add_argument("krw_amount", type=float)
    buy_market.add_argument("--execute", action="store_true")

    sell_market = commands.add_parser("sell-market", help="Place or simulate a market sell.")
    sell_market.add_argument("market")
    sell_market.add_argument("volume", type=float)
    sell_market.add_argument("--execute", action="store_true")

    cancel = commands.add_parser("cancel", help="Cancel or simulate canceling an order.")
    cancel.add_argument("uuid")
    cancel.add_argument("--execute", action="store_true")

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    load_env_file(args.env_file)
    settings = load_settings(require_keys=args.command in KEY_REQUIRED_COMMANDS)
    system = UpbitOrderSystem(settings)

    result = dispatch(system, args)
    print_result(result)


def dispatch(system: UpbitOrderSystem, args: argparse.Namespace) -> Any:
    if args.command == "markets":
        return system.list_markets(fiat=args.fiat)
    if args.command == "price":
        markets = args.markets or [system.settings.default_market]
        return system.current_price(markets[0] if len(markets) == 1 else markets)
    if args.command == "candles":
        market = args.market or system.settings.default_market
        return system.candles(market=market, interval=args.interval, count=args.count)
    if args.command == "balances":
        return system.balances()
    if args.command == "buy-limit":
        return system.buy_limit(args.market, args.price, args.volume, execute=args.execute)
    if args.command == "sell-limit":
        return system.sell_limit(args.market, args.price, args.volume, execute=args.execute)
    if args.command == "buy-market":
        return system.buy_market(args.market, args.krw_amount, execute=args.execute)
    if args.command == "sell-market":
        return system.sell_market(args.market, args.volume, execute=args.execute)
    if args.command == "cancel":
        return system.cancel(args.uuid, execute=args.execute)

    raise ValueError(f"Unsupported command: {args.command}")


def print_result(result: Any) -> None:
    if hasattr(result, "to_string"):
        print(result.to_string())
        return
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))


KEY_REQUIRED_COMMANDS = {
    "balances",
}


if __name__ == "__main__":
    main()
