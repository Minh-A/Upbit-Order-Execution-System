# Upbit Order Execution System

Secure Python utilities for Upbit market data lookup, account balance checks, and
guarded order execution. This project is best described as an **Upbit API order
execution layer for crypto quant trading workflows** rather than a complete
strategy engine.

## Features

- KRW market ticker lookup
- Current price lookup for one or more markets
- OHLCV candle retrieval
- Private balance lookup through environment-based API credentials
- Limit buy/sell, market buy/sell, and order cancel commands
- Dry-run mode enabled by default to prevent accidental live orders
- Public-safe structure with no API keys in source code

## Project Structure

```text
.
|-- main.py                 # CLI entry point
|-- order.py                # Backward-compatible entry point
|-- order1.py               # Backward-compatible entry point
|-- upbit_order/
|   |-- config.py           # Environment and settings loader
|   |-- client.py           # pyupbit client creation
|   `-- system.py           # Market data and guarded order execution
|-- docs/
|   `-- security-cleanup.md # Removed-sensitive-data notes
|-- .env.example
|-- .gitignore
|-- LICENSE
`-- requirements.txt
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Fill `.env` locally:

```bash
UPBIT_ACCESS_KEY=your-access-key
UPBIT_SECRET_KEY=your-secret-key
UPBIT_DEFAULT_MARKET=KRW-BTC
UPBIT_DRY_RUN=true
```

`.env` is ignored by git and must not be committed.

## Usage

Public market data does not require API credentials:

```bash
python main.py markets
python main.py price KRW-BTC KRW-ETH
python main.py candles --market KRW-BTC --interval minute1 --count 20
```

Private account calls require local credentials:

```bash
python main.py balances
```

Order commands are simulated by default:

```bash
python main.py buy-limit KRW-BTC 50000000 0.001
python main.py sell-limit KRW-BTC 70000000 0.001
python main.py buy-market KRW-BTC 10000
python main.py sell-market KRW-BTC 0.001
python main.py cancel <order-uuid>
```

To send a real order, both conditions must be true:

```bash
UPBIT_DRY_RUN=false
python main.py buy-market KRW-BTC 10000 --execute
```

This two-step guard is intentional.

## Security Notes

- No Upbit access key or secret key is stored in this repository.
- Local credential files such as `key.txt`, `.env`, and token files are ignored.
- The original local key files were removed from the public project.
- Rotate any API keys that were previously stored in local files before live use.

## License

MIT License
