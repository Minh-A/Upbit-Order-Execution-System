"""Market data and guarded order execution for Upbit."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from .client import create_private_client, pyupbit_module
from .config import UpbitSettings


class UpbitOrderSystem:
    """Upbit API execution layer with dry-run protection by default."""

    def __init__(self, settings: UpbitSettings):
        self.settings = settings

    def list_markets(self, fiat: str = "KRW") -> list[str]:
        pyupbit = pyupbit_module()
        return pyupbit.get_tickers(fiat=fiat)

    def current_price(self, markets: str | list[str]) -> Any:
        pyupbit = pyupbit_module()
        return pyupbit.get_current_price(markets)

    def candles(self, market: str, interval: str = "minute1", count: int = 20):
        pyupbit = pyupbit_module()
        return pyupbit.get_ohlcv(market, interval=interval, count=count)

    def balances(self) -> Any:
        client = create_private_client(self.settings)
        return client.get_balances()

    def buy_limit(self, market: str, price: float, volume: float, execute: bool = False) -> Any:
        payload = {
            "side": "bid",
            "order_type": "limit",
            "market": market,
            "price": price,
            "volume": volume,
        }
        if self._is_dry_run(execute):
            return self._dry_run_payload(payload)

        client = create_private_client(self.settings)
        return client.buy_limit_order(market, price, volume)

    def sell_limit(self, market: str, price: float, volume: float, execute: bool = False) -> Any:
        payload = {
            "side": "ask",
            "order_type": "limit",
            "market": market,
            "price": price,
            "volume": volume,
        }
        if self._is_dry_run(execute):
            return self._dry_run_payload(payload)

        client = create_private_client(self.settings)
        return client.sell_limit_order(market, price, volume)

    def buy_market(self, market: str, krw_amount: float, execute: bool = False) -> Any:
        payload = {
            "side": "bid",
            "order_type": "market",
            "market": market,
            "krw_amount": krw_amount,
        }
        if self._is_dry_run(execute):
            return self._dry_run_payload(payload)

        client = create_private_client(self.settings)
        return client.buy_market_order(market, krw_amount)

    def sell_market(self, market: str, volume: float, execute: bool = False) -> Any:
        payload = {
            "side": "ask",
            "order_type": "market",
            "market": market,
            "volume": volume,
        }
        if self._is_dry_run(execute):
            return self._dry_run_payload(payload)

        client = create_private_client(self.settings)
        return client.sell_market_order(market, volume)

    def cancel(self, uuid: str, execute: bool = False) -> Any:
        payload = {"action": "cancel", "uuid": uuid}
        if self._is_dry_run(execute):
            return self._dry_run_payload(payload)

        client = create_private_client(self.settings)
        return client.cancel_order(uuid)

    def _is_dry_run(self, execute: bool) -> bool:
        return self.settings.dry_run or not execute

    def _dry_run_payload(self, payload: dict[str, Any]) -> dict[str, Any]:
        return {
            "dry_run": True,
            "settings": {
                **asdict(self.settings),
                "access_key": _mask_secret(self.settings.access_key),
                "secret_key": _mask_secret(self.settings.secret_key),
            },
            "order": payload,
        }


def _mask_secret(value: str) -> str:
    if not value:
        return ""
    if len(value) <= 8:
        return "*" * len(value)
    return f"{value[:4]}{'*' * (len(value) - 8)}{value[-4:]}"
