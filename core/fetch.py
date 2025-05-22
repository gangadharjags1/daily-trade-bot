# core/fetch.py

from core.robinhood_fetcher import (
    login_robinhood,
    get_robinhood_crypto_data,
    get_robinhood_stock_data,
    is_crypto_symbol
)

def fetch_stock_data(symbol):
    if is_crypto_symbol(symbol):
        result = get_robinhood_crypto_data(symbol)
    else:
        result = get_robinhood_stock_data(symbol)

    if not result:
        return None

    # Ensure required fields are present
    if all(key in result for key in ["close", "high", "low", "date"]):
        return result
    else:
        return None
