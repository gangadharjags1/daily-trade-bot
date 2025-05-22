# core/robinhood_fetcher.py

import os
from datetime import datetime, timedelta
from robin_stocks import robinhood as r
from dotenv import load_dotenv

load_dotenv()

def login_robinhood():
    try:
        r.authentication.login(
            username=os.getenv("ROBINHOOD_USERNAME"),
            password=os.getenv("ROBINHOOD_PASSWORD"),
            expiresIn=86400,
            store_session=True
        )
        print("✅ Robinhood login successful.")
    except Exception as e:
        print(f"❌ Robinhood login failed: {e}")

def is_crypto_symbol(symbol):
    return "/" in symbol and symbol.endswith("USD")

def get_robinhood_crypto_data(symbol):
    try:
        base = symbol.split("/")[0].upper()
        quote_data = r.crypto.get_crypto_quote(base)
        if not quote_data or "mark_price" not in quote_data:
            print(f"[Robinhood Fetch Error] {symbol}: Invalid crypto quote")
            return None

        mark_price = float(quote_data["mark_price"])

        # simulate 30-day fake candle data
        closes = [mark_price] * 30
        highs = [mark_price * 1.01] * 30
        lows = [mark_price * 0.99] * 30
        dates = [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(30)][::-1]

        return {
            "close": closes,
            "high": highs,
            "low": lows,
            "date": dates
        }

    except Exception as e:
        print(f"[Robinhood Fetch Error] {symbol}: {e}")
        return None

def get_robinhood_stock_data(symbol):
    try:
        quote_data = r.stocks.get_quotes(symbol)
        if not quote_data or "last_trade_price" not in quote_data[0]:
            print(f"[Robinhood Fetch Error] {symbol}: Invalid stock quote")
            return None

        price = float(quote_data[0]["last_trade_price"])

        closes = [price] * 30
        highs = [price * 1.01] * 30
        lows = [price * 0.99] * 30
        dates = [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(30)][::-1]

        return {
            "close": closes,
            "high": highs,
            "low": lows,
            "date": dates
        }

    except Exception as e:
        print(f"[Robinhood Fetch Error] {symbol}: {e}")
        return None
