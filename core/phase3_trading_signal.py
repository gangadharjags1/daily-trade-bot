# core/phase3_trading_signal.py

from core.fetch import fetch_stock_data
from core.strategy import analyze_signals
from core.robinhood_fetcher import is_crypto_symbol

def run_trading_signals(symbols):
    results = []

    for symbol in symbols:
        print(f"🔁 Processing {symbol}...")
        is_crypto = is_crypto_symbol(symbol)

        try:
            data = fetch_stock_data(symbol)
            if data is None:
                print(f"❌ Skipping {symbol}: No price")
                results.append((None, "No price"))
                continue

            signal, reason = analyze_signals(data, symbol)
            if signal:
                print(f"✅ Signal found for {symbol}: {signal['direction']} at {signal['entry']}")
            else:
                print(f"⚠️ {reason}")
            results.append((signal, reason))

        except Exception as e:
            print(f"[Signal Sender Error] {symbol}: {e}")
            results.append((None, str(e)))

    return results
