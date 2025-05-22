# backtest_runner.py

from core.backtester import run_backtest

# Use any 5 general stock symbols
sample_stocks = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN"]

# Run backtest for the last 30 trading days
run_backtest(sample_stocks, days=30)
