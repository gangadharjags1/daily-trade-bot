# core/report_exporter.py

import os
import pandas as pd
from datetime import datetime, timedelta

last_excel_export_time = None

def export_signals_to_excel(signals, interval_minutes=180):
    global last_excel_export_time

    now = datetime.now()
    if last_excel_export_time and (now - last_excel_export_time) < timedelta(minutes=interval_minutes):
        print(f"⏱️ Excel export skipped — will export again at {last_excel_export_time + timedelta(minutes=interval_minutes)}")
        return None

    os.makedirs("exports", exist_ok=True)
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"exports/daily_trade_report_{timestamp}.xlsx"

    rows = []
    for signal in signals:
        rows.append({
            "Symbol": signal["symbol"],
            "Direction": signal["direction"],
            "Entry": signal["entry"],
            "Target": signal["target"],
            "Stop": signal["stop"],
            "Confidence": f"{signal['confidence']}%",
            "Insight": signal["insight"],
            "Time": signal["time"]
        })

    df = pd.DataFrame(rows)
    df.to_excel(filename, index=False)
    last_excel_export_time = now
    print(f"✅ Exported Excel to: {filename}")
    return filename
