"""Configuration helpers for the Upbit order system."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path


TRUE_VALUES = {"1", "true", "yes", "on"}
FALSE_VALUES = {"0", "false", "no", "off"}


@dataclass(frozen=True)
class UpbitSettings:
    access_key: str
    secret_key: str
    default_market: str
    dry_run: bool


def load_env_file(path: str | Path = ".env") -> None:
    env_path = Path(path)
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            os.environ.setdefault(key, value)


def load_settings(require_keys: bool = False) -> UpbitSettings:
    access_key = os.getenv("UPBIT_ACCESS_KEY", "").strip()
    secret_key = os.getenv("UPBIT_SECRET_KEY", "").strip()
    default_market = os.getenv("UPBIT_DEFAULT_MARKET", "KRW-BTC").strip() or "KRW-BTC"
    dry_run = _read_bool("UPBIT_DRY_RUN", default=True)

    if require_keys and (not access_key or not secret_key):
        raise RuntimeError(
            "UPBIT_ACCESS_KEY and UPBIT_SECRET_KEY must be configured for private API calls."
        )

    return UpbitSettings(
        access_key=access_key,
        secret_key=secret_key,
        default_market=default_market,
        dry_run=dry_run,
    )


def _read_bool(name: str, default: bool) -> bool:
    raw_value = os.getenv(name)
    if raw_value is None:
        return default

    normalized = raw_value.strip().lower()
    if normalized in TRUE_VALUES:
        return True
    if normalized in FALSE_VALUES:
        return False
    return default
