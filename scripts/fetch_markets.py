#!/usr/bin/env python3
import json
from datetime import datetime, timezone
import math

import yfinance as yf

TICKERS = [
    ("AAPL", "Apple Inc."),
    ("MSFT", "Microsoft Corp."),
    ("GOOGL", "Alphabet Inc."),
    ("AMZN", "Amazon.com, Inc."),
    ("NVDA", "NVIDIA Corp."),
    ("META", "Meta Platforms, Inc."),
    ("TSLA", "Tesla, Inc.")
]

def get_quote(ticker):
    t = yf.Ticker(ticker)
    # Use last 2 daily closes to compute change
    hist = t.history(period="5d", interval="1d")
    price = None
    prev = None
    if not hist.empty:
        price = float(hist["Close"].iloc[-1])
        if len(hist["Close"]) >= 2:
            prev = float(hist["Close"].iloc[-2])
    # Fallbacks
    if price is None:
        finfo = getattr(t, "fast_info", {}) or {}
        price = float(finfo.get("last_price", 0.0))
        prev = float(finfo.get("previous_close", 0.0))
    change = (price - prev) if (price is not None and prev is not None and prev != 0) else 0.0
    percent = (change / prev * 100.0) if (prev not in (None, 0)) else 0.0
    info = t.get_info() if hasattr(t, "get_info") else {}
    exchange = info.get("exchange", "") or info.get("fullExchangeName", "") or "NASDAQ"
    return price, change, percent, exchange

def main():
    items = []
    for sym, name in TICKERS:
        try:
            price, change, percent, exch = get_quote(sym)
            items.append({
                "ticker": sym,
                "name": name,
                "price": round(price, 2),
                "change": round(change, 2),
                "percent": round(percent, 2),
                "exchange": exch
            })
        except Exception as e:
            items.append({
                "ticker": sym,
                "name": name,
                "price": 0, "change": 0, "percent": 0,
                "exchange": "N/A", "error": str(e)
            })
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "items": items
    }
    with open("markets/markets.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"Wrote markets/markets.json with {len(items)} tickers")

if __name__ == "__main__":
    main()
