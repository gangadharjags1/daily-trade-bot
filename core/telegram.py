import requests
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_signal_report(signals):
    if not signals:
        print("❌ No signals to send.")
        return

    message = "📊 *Dual-Direction Daily Trade Signals*\n\n"

    for s in signals[:10]:  # Top 10 best signals
        symbol = s.get("symbol", "")
        price = s.get("price", "N/A")
        time_frame = s.get("time_frame", "Intraday")

        # Long setup
        long = s.get("long", {})
        long_entry = long.get("entry_price", "N/A")
        long_target = long.get("target", "N/A")
        long_stop = long.get("stop_loss", "N/A")
        long_conf = long.get("confidence", "N/A")
        long_ai = long.get("ai_insight", "No insight")

        # Short setup
        short = s.get("short", {})
        short_entry = short.get("entry_price", "N/A")
        short_target = short.get("target", "N/A")
        short_stop = short.get("stop_loss", "N/A")
        short_conf = short.get("confidence", "N/A")
        short_ai = short.get("ai_insight", "No insight")

        message += f"📈 *{symbol}*  • Current Price: ${price}  • Time Frame: {time_frame}\n\n"

        message += f"🟩 *LONG Setup*\n"
        message += f"• Entry above: ${long_entry}\n"
        message += f"• Target: ${long_target}\n"
        message += f"• Stop-Loss: ${long_stop}\n"
        message += f"• Confidence: {long_conf}%\n"
        message += f"💬 _{long_ai}_\n\n"

        message += f"🟥 *SHORT Setup*\n"
        message += f"• Entry below: ${short_entry}\n"
        message += f"• Target: ${short_target}\n"
        message += f"• Stop-Loss: ${short_stop}\n"
        message += f"• Confidence: {short_conf}%\n"
        message += f"💬 _{short_ai}_\n\n"

        message += "—" * 25 + "\n\n"

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    response = requests.post(url, data=payload)

    if response.status_code == 200:
        print("✅ Signal report sent to Telegram.")
    else:
        print(f"❌ Telegram error: {response.text}")
