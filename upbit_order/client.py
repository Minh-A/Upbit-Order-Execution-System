"""Thin wrapper around pyupbit imports and authenticated client creation."""

from __future__ import annotations

from .config import UpbitSettings


def pyupbit_module():
    try:
        import pyupbit
    except ImportError as exc:
        raise RuntimeError("Install dependencies with `pip install -r requirements.txt`.") from exc
    return pyupbit


def create_private_client(settings: UpbitSettings):
    if not settings.access_key or not settings.secret_key:
        raise RuntimeError(
            "Private API calls require UPBIT_ACCESS_KEY and UPBIT_SECRET_KEY."
        )

    pyupbit = pyupbit_module()
    return pyupbit.Upbit(settings.access_key, settings.secret_key)
