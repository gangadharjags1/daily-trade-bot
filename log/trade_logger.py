import csv
from datetime import datetime

def log_signal(ticker, indicators, report):
    with open("log/backtest_trade_log.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now().isoformat(),               # timestamp
            ticker,                                   # ticker symbol
            report.get("price", indicators.get("close", 0)),  # entry price
            report["confidence"],                    # confidence %
            report["target_price"],                  # target price
            report["stop_loss"],                     # stop loss
            report["text"]                           # signal summary text
        ])
