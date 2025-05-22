# core/backtester.py

import os
from datetime import datetime, timedelta
from core.strategy import analyze_signals
from core.robinhood_fetcher import get_robinhood_price

def run_backtest(symbols, days=30):
    print("Starting login process...")
    from robin_stocks import robinhood as r
    r.authentication.login(
        username=os.getenv("ROBINHOOD_USERNAME"),
        password=os.getenv("ROBINHOOD_PASSWORD"),
        expiresIn=86400,
        store_session=True
    )
    print("✅ Robinhood login successful.")

    today = datetime.today()
    start_date = today - timedelta(days=days)

    all_results = []

    for symbol in symbols:
        print(f"🔁 Backtesting {symbol}...")

        price = get_robinhood_price(symbol)
        if not price:
            print(f"❌ Skipping {symbol}: No price")
            continue

        # Fake daily prices with slight variations
        mock_data = {
            "Time Series (Daily)": {
                (today - timedelta(i)).strftime("%Y-%m-%d"): {
                    "4. close": f"{price * (1 + (i - days/2) / 500):.2f}"
                }
                for i in range(days)
            },
            "realtime_price": f"{price:.2f}"
        }

        result = analyze_signals(symbol, mock_data)
        if result:
            all_results.append(result)

    if not all_results:
        print("⚠️ No trades found in backtest.")
    else:
        print(f"✅ Backtest complete for {len(all_results)} symbols.")
        for r in all_results:
            print(f"{r['symbol']} → BUY {r['long']['entry_price']} → Target {r['long']['target']}")
