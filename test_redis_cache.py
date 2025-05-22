import requests
import os

# These should already be set in your .env or environment
UPSTASH_REDIS_REST_URL = os.getenv("UPSTASH_REDIS_REST_URL")
UPSTASH_REDIS_REST_TOKEN = os.getenv("UPSTASH_REDIS_REST_TOKEN")

def get_from_cache(symbol):
    response = requests.post(
        f"{UPSTASH_REDIS_REST_URL}/get/{symbol}",
        headers={"Authorization": f"Bearer {UPSTASH_REDIS_REST_TOKEN}"}
    )
    return response.json()

def list_keys():
    response = requests.post(
        f"{UPSTASH_REDIS_REST_URL}/keys",
        headers={"Authorization": f"Bearer {UPSTASH_REDIS_REST_TOKEN}"}
    )
    return response.json()

# 🔍 List all cached stock tickers
print("📦 Redis Keys:")
print(list_keys())

# 🔍 Fetch cached data for AAPL
print("\n📉 Cached AAPL data:")
print(get_from_cache("AAPL"))

