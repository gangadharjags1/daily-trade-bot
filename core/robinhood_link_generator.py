# core/robinhood_link_generator.py

def generate_robinhood_trade_link(symbol, action, quantity=1):
    """
    Generates a Robinhood web URL to place a trade manually.

    Parameters:
    - symbol: str, e.g. 'AAPL' or 'BTC'
    - action: str, either 'buy' or 'sell'
    - quantity: int or float, the number of shares or crypto units

    Returns:
    - URL string to open Robinhood trade page
    """
    action = action.lower()
    if action not in ['buy', 'sell']:
        raise ValueError("Action must be 'buy' or 'sell'")

    # Robinhood uses hyphen instead of dot for class B stocks like BRK-B
    normalized_symbol = symbol.replace('.', '-')

    # For crypto, Robinhood uses lowercase symbols and adds '-usd'
    if '/' in symbol or symbol.endswith('USD'):
        base = symbol.split('/')[0].lower()
        normalized_symbol = f"{base}-usd"
        return f"https://robinhood.com/crypto/{normalized_symbol}"

    return f"https://robinhood.com/stocks/{normalized_symbol}"
