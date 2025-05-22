from fastapi import FastAPI
import requests
import os
import json
from dotenv import load_dotenv  # ← ADD THIS

load_dotenv()  # ← AND THIS

app = FastAPI()

REDIS_REST_URL = os.getenv("UPSTASH_REDIS_REST_URL")
REDIS_REST_TOKEN = os.getenv("UPSTASH_REDIS_REST_TOKEN")
TWELVE_DATA_API_KEY = os.getenv("TWELVE_DATA_API_KEY")

@app.get("/price/{symbol}")
def get_stock_price(symbol: str):
    cache_key = f"price:{symbol}"

    try:
        # Step 1: Check Redis Cache
        redis_resp = requests.post(
            f"{REDIS_REST_URL}/get/{cache_key}",
            headers={"Authorization": f"Bearer {REDIS_REST_TOKEN}"}
        )
        redis_data = redis_resp.json()
        if redis_data.get("result"):
            return {"source": "cache", "data": json.loads(redis_data["result"])}

        # Step 2: Fetch from TwelveData
        url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=1min&outputsize=5&apikey={TWELVE_DATA_API_KEY}"
        api_resp = requests.get(url).json()
        if "status" in api_resp and api_resp["status"] == "error":
            return {"error": api_resp}

        # Step 3: Cache the new response
        requests.post(
            f"{REDIS_REST_URL}/set/{cache_key}",
            headers={"Authorization": f"Bearer {REDIS_REST_TOKEN}"},
            data=json.dumps({"value": json.dumps(api_resp), "expiration": 300})  # 5 minutes
        )

        return {"source": "live", "data": api_resp}
    except Exception as e:
        return {"error": str(e)}
