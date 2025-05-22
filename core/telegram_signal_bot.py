# core/telegram_signal_bot.py

import os
import requests
from dotenv import load_dotenv
from core.telegram_formatter import format_telegram_message

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_signals_to_telegram(signals):
    if not signals:
        print("❌ No signals to send.")
        return

    for signal in signals:
        try:
            message = format_telegram_message(signal)
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
            response = requests.post(url, data={
                "chat_id": CHAT_ID,
                "text": message,
                "parse_mode": "HTML",
                "disable_web_page_preview": False
            })
            if response.status_code != 200:
                print(f"⚠️ Telegram Error ({signal['symbol']}):", response.text)
            else:
                print(f"✅ Sent to Telegram: {signal['symbol']}")

        except Exception as e:
            print(f"[Telegram Send Error] {signal['symbol']}: {e}")
