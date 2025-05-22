import os
import requests
import json

def generate_ai_summary(ticker, indicators):
    try:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            return "⚠️ Groq API key missing."

        prompt = (
            f"Stock: {ticker}\n"
            f"Price: {indicators.get('close')}\n"
            f"RSI: {indicators.get('rsi')}\n"
            f"MACD Histogram: {indicators.get('macd_hist')}\n"
            f"ATR: {indicators.get('atr')}\n"
            f"Confidence Score: {indicators.get('confidence', '?')}\n"
            "Based on these technical indicators, provide a short AI trading insight in 2 sentences. "
            "Include a directional prediction (up/down), confidence score, and market tone (bullish/bearish/neutral)."
        )

        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "llama3-70b-8192",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.5
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code != 200:
            return f"⚠️ Groq HTTP Error: {response.status_code} - {response.text}"

        result = response.json()
        return result["choices"][0]["message"]["content"].strip()

    except Exception as e:
        return f"⚠️ Groq AI summary error: {e}"
