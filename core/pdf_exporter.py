from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from datetime import datetime

def export_signals_to_pdf(signals, output_dir="exports"):
    os.makedirs(output_dir, exist_ok=True)
    filename = f"daily_trade_report_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.pdf"
    filepath = os.path.join(output_dir, filename)

    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter

    y = height - 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "📊 Daily Trade Signals (Dual Direction)")
    y -= 30

    for s in signals:
        symbol = s.get("symbol", "")
        price = s.get("price", "N/A")
        time_frame = s.get("time_frame", "Intraday")

        long = s.get("long", {})
        short = s.get("short", {})

        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, f"{symbol} — {time_frame} (Price: ${price})")
        y -= 20

        c.setFont("Helvetica", 10)
        c.drawString(60, y, f"🟩 LONG: Entry ${long.get('entry_price')}, Target ${long.get('target')}, Stop ${long.get('stop_loss')}, Confidence {long.get('confidence')}%")
        y -= 15
        c.drawString(60, y, f"Insight: {long.get('ai_insight')}")
        y -= 30

        c.drawString(60, y, f"🟥 SHORT: Entry ${short.get('entry_price')}, Target ${short.get('target')}, Stop ${short.get('stop_loss')}, Confidence {short.get('confidence')}%")
        y -= 15
        c.drawString(60, y, f"Insight: {short.get('ai_insight')}")
        y -= 40

        if y < 100:
            c.showPage()
            y = height - 50

    c.save()
    return filepath
