#!/usr/bin/env python3
from __future__ import annotations

import sys
from datetime import datetime
from typing import Any

import yfinance as yf


TICKER = "0700.HK"
COMPANY_NAME = "Tencent Holdings"


def _format_timestamp(value: Any) -> str:
    if value is None:
        return "N/A"

    if hasattr(value, "to_pydatetime"):
        value = value.to_pydatetime()

    if isinstance(value, datetime):
        return value.isoformat(sep=" ", timespec="seconds")

    return str(value)


def _extract_currency(stock: yf.Ticker, metadata: dict[str, Any]) -> str:
    currency = metadata.get("currency")
    if currency:
        return str(currency)

    fast_info = stock.fast_info
    if hasattr(fast_info, "get"):
        currency = fast_info.get("currency")
        if currency:
            return str(currency)

    return "N/A"


def get_latest_price(ticker: str) -> tuple[float, str, Any]:
    stock = yf.Ticker(ticker)
    history = stock.history(period="1d", interval="1m", auto_adjust=False)
    if history.empty:
        history = stock.history(period="5d", interval="1d", auto_adjust=False)

    if history.empty:
        raise RuntimeError(f"No market data returned for {ticker}")

    metadata = stock.get_history_metadata()
    latest = history.iloc[-1]
    timestamp = history.index[-1]

    try:
        price = float(latest["Close"])
    except (TypeError, ValueError, KeyError) as exc:
        raise RuntimeError(f"Unable to parse latest price for {ticker}") from exc

    currency = _extract_currency(stock, metadata if isinstance(metadata, dict) else {})
    return price, currency, timestamp


def main() -> int:
    try:
        price, currency, timestamp = get_latest_price(TICKER)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(f"{COMPANY_NAME} latest price")
    print(f"Ticker: {TICKER}")
    print(f"Price: {price:.2f}")
    print(f"Currency: {currency}")
    print(f"Timestamp: {_format_timestamp(timestamp)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
