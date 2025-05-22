import os
import requests

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_trade_signal_to_telegram(signal):
    try:
        symbol = signal.get("symbol")
        direction = signal.get("direction", "").upper()
        price = signal.get("price")

        long = signal.get("long", {})
        short = signal.get("short", {})

        msg = f"📊 *{symbol}* — Intraday Signal (Price: ${price})\n"
        msg += f"\n▶️ *LONG Entry*: ${long.get('entry_price')}, 🎯 Target: ${long.get('target')}, 🛑 Stop: ${long.get('stop_loss')} ({long.get('confidence')}% confidence)"
        msg += f"\n💬 {long.get('ai_insight')}"
        msg += f"\n\n🔻 *SHORT Entry*: ${short.get('entry_price')}, 🎯 Target: ${short.get('target')}, 🛑 Stop: ${short.get('stop_loss')} ({short.get('confidence')}% confidence)"
        msg += f"\n💬 {short.get('ai_insight')}"

        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": msg,
            "parse_mode": "Markdown"
        }

        res = requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", json=payload)
        if res.status_code == 200:
            print(f"✅ Signal sent for {symbol}")
        else:
            print(f"❌ Failed to send signal for {symbol}: {res.text}")

    except Exception as e:
        print(f"[Signal Sender Error] {e}")
