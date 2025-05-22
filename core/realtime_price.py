from playwright.sync_api import sync_playwright

def get_realtime_price(symbol):
    try:
        url = f"https://www.tradingview.com/symbols/{symbol.upper()}/"
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=10000)
            page.wait_for_selector("div[data-symbol]", timeout=10000)

            price_el = page.query_selector("div[data-symbol] span[data-field='value']")
            if price_el:
                price = price_el.inner_text().replace(',', '')
                return float(price)
            else:
                print(f"[REALTIME FAIL] Could not find live price for {symbol}")
                return None
    except Exception as e:
        print(f"[REALTIME ERROR] {symbol}: {e}")
        return None
