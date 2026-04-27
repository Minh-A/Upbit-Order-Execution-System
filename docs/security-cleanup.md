# Security Cleanup

This repository previously mixed public sample code with private Upbit credentials.
The public version removes those secrets and keeps only a safe execution template.

## Removed

- Removed hard-coded Upbit access and secret keys from `order.py`.
- Removed commented credentials from `order1.py`.
- Removed local key files from the project:
  - `key.txt`
  - Korean-named key text file
- Removed local Windows output paths from public code.

## Replaced With

- `UPBIT_ACCESS_KEY` and `UPBIT_SECRET_KEY` environment variables.
- `.env.example` with empty placeholders only.
- `.gitignore` rules for `.env`, key files, token files, local data, and generated outputs.
- Dry-run order execution by default. Real orders require both `UPBIT_DRY_RUN=false`
  and the command-level `--execute` flag.

## Recommended Key Action

Because the original keys were present in local files and source code, rotate the
Upbit API keys in the Upbit console before using this repository again.
