import httpx
import json
import hashlib

# Upstash Redis credentials
UPSTASH_REDIS_URL = "https://glowing-robin-12590.upstash.io"
UPSTASH_REDIS_TOKEN = "ATEuAAIjcDFkMDMzZDhkYzY4NGU0ZTZiODVhYzRkYTllZjY5NzBhMXAxMA"

HEADERS = {
    "Authorization": f"Bearer {UPSTASH_REDIS_TOKEN}"
}

def _hash_key(key):
    return hashlib.sha1(key.encode()).hexdigest()

def redis_get(symbol):
    hashed_key = _hash_key(symbol)
    url = f"{UPSTASH_REDIS_URL}/get/{hashed_key}"
    try:
        response = httpx.get(url, headers=HEADERS, timeout=10.0)
        if response.status_code == 200:
            value = response.json().get("result")
            if value:
                return json.loads(value)
    except Exception as e:
        print(f"Redis GET error for {symbol}: {e}")
    return None

def redis_set(symbol, data, ttl=86400):
    hashed_key = _hash_key(symbol)
    payload = json.dumps(data)
    url = f"{UPSTASH_REDIS_URL}/set/{hashed_key}"
    try:
        response = httpx.post(url, headers=HEADERS, params={"EX": ttl}, content=payload, timeout=10.0)
        return response.status_code == 200
    except Exception as e:
        print(f"Redis SET error for {symbol}: {e}")
        return False
