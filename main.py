# main.py

from core.phase3_trading_signal import run_trading_signals
from top_all_robinhood_crypto import top_all_crypto
from top_all_robinhood_stocks import top_all_stocks
from core.report_exporter import export_signals_to_excel
from core.pdf_exporter import export_signals_to_pdf
from core.telegram_pdf import send_pdf_to_telegram
from core.robinhood_fetcher import login_robinhood
from datetime import datetime

if __name__ == "__main__":
    print("Starting login process...")
    login_robinhood()

    all_symbols = top_all_crypto + top_all_stocks

    print(f"\n⏱️ Running bot at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}...")

    signal_results = run_trading_signals(all_symbols)

    # ✅ Only keep successful signals (non-None)
    signals = [s for s, _ in signal_results if s is not None]

    if signals:
        export_signals_to_excel(signals)
        pdf_path = export_signals_to_pdf(signals)
        send_pdf_to_telegram(pdf_path)
    else:
        print("⚠️ No valid trading signals found this cycle.")
