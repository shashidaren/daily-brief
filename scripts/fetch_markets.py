#!/usr/bin/env python3
import json
import os
from datetime import datetime, timezone
import yfinance as yf

TECH = [
    ("AAPL", "Apple Inc."), ("MSFT", "Microsoft Corp."), ("GOOGL", "Alphabet Inc."),
    ("AMZN", "Amazon.com, Inc."), ("NVDA", "NVIDIA Corp."), ("META", "Meta Platforms"),
    ("TSLA", "Tesla, Inc."), ("AMD", "Advanced Micro Devices"), ("ORCL", "Oracle Corp."),
    ("IBM", "IBM"), ("INTC", "Intel Corp.")
]

MYX = [
    ("1155K.KL", "Malayan Banking (Maybank)"), ("1023.KL", "CIMB Group"),
    ("5347.KL", "Tenaga Nasional"), ("5681.KL", "Petronas Dagangan"),
    ("7113.KL", "Top Glove"), ("3182.KL", "Genting Bhd"),
    ("6888.KL", "Axiata Group"), ("6947.KL", "Digi.Com Bhd")
]

METALS = [("XAUUSD=X", "Gold Spot USD"), ("XAGUSD=X", "Silver Spot USD")]

TICKERS = TECH + MYX + METALS


def get_quote(sym):
    t = yf.Ticker(sym)
    price = prev = None
    hist = t.history(period="5d", interval="1d")

    if not hist.empty:
        price = float(hist["Close"].iloc[-1])
        if len(hist["Close"]) >= 2:
            prev = float(hist["Close"].iloc[-2])

    if price is None:
        finfo = getattr(t, "fast_info", {}) or {}
        price = float(finfo.get("last_price", 0.0))
        prev = float(finfo.get("previous_close", 0.0))

    change = (price - prev) if (price is not None and prev not in (None, 0)) else 0.0
    percent = (change / prev * 100.0) if (prev not in (None, 0)) else 0.0

    # use .info instead of get_info (deprecated in new versions)
    info = getattr(t, "info", {}) or {}
    exchange = info.get("exchange", "") or info.get("fullExchangeName", "") or "—"

    return round(price or 0.0, 2), round(change, 2), round(percent, 2), exchange


def main():
    items = []
    for sym, name in TICKERS:
        try:
            price, change, percent, exch = get_quote(sym)
            items.append({
                "ticker": sym, "name": name, "price": price,
                "change": change, "percent": percent, "exchange": exch
            })
        except Exception as e:
            items.append({
                "ticker": sym, "name": name, "price": 0,
                "change": 0, "percent": 0, "exchange": "N/A",
                "error": str(e)
            })

    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "items": items
    }

    os.makedirs("markets", exist_ok=True)
    with open("markets/markets.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"Wrote markets/markets.json with {len(items)} tickers")


if __name__ == "__main__":
    main()
