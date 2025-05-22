
# core/telegram_formatter.py

from core.robinhood_link_generator import generate_robinhood_trade_link

def format_telegram_message(signal):
    sym = signal['symbol']
    price = signal['price']
    direction = signal['direction']
    tf = signal['time_frame']

    msg = f"📈 <b>{sym}</b> — <i>{tf} (Price: ${price})</i>\n"

    if 'long' in signal:
        l = signal['long']
        buy_link = generate_robinhood_trade_link(sym, "buy")
        msg += (
            f"\n<b>■ LONG</b>: Entry ${l['entry_price']}, "
            f"Target ${l['target']}, Stop ${l['stop_loss']}, Confidence {l['confidence']}%\n"
            f"<i>{l['ai_insight']}</i>\n"
            f"<a href='{buy_link}'>🚀 Execute BUY on Robinhood</a>\n"
        )

    if 'short' in signal:
        s = signal['short']
        sell_link = generate_robinhood_trade_link(sym, "sell")
        msg += (
            f"\n<b>■ SHORT</b>: Entry ${s['entry_price']}, "
            f"Target ${s['target']}, Stop ${s['stop_loss']}, Confidence {s['confidence']}%\n"
            f"<i>{s['ai_insight']}</i>\n"
            f"<a href='{sell_link}'>🔻 Execute SELL on Robinhood</a>\n"
        )

    return msg
