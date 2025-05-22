import requests
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_pdf_to_telegram(filepath):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    with open(filepath, "rb") as f:
        files = {"document": f}
        data = {"chat_id": CHAT_ID, "caption": "📊 Dual-Direction Daily Trade Report"}
        response = requests.post(url, files=files, data=data)

    if response.status_code == 200:
        print("✅ PDF report sent to Telegram.")
    else:
        print(f"❌ Telegram error: {response.text}")
