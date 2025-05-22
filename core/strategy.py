# core/strategy.py
from core.indicators import calculate_rsi, calculate_macd, calculate_atr
from core.indicators import calculate_rsi, calculate_macd
from datetime import datetime
import numpy as np
import json
import os

# === Confidence Calculator ===
def calculate_confidence(rsi, macd, signal, atr, price):
    confidence = 0

    # RSI strength
    if 55 <= rsi <= 65:
        confidence += 20
    elif 65 < rsi <= 75 or 45 <= rsi < 55:
        confidence += 10

    # MACD strength
    macd_distance = abs(macd - signal)
    if macd_distance > 0.5:
        confidence += 20
    elif macd_distance > 0.2:
        confidence += 10

    # ATR volatility level
    atr_percent = atr / price
    if 0.01 <= atr_percent <= 0.03:
        confidence += 20
    elif 0.005 <= atr_percent < 0.01:
        confidence += 10

    # Entry-Target distance strength
    reward_risk_ratio = (atr * 1.5) / (atr * 0.75)
    if reward_risk_ratio >= 2:
        confidence += 20
    elif reward_risk_ratio >= 1.5:
        confidence += 10

    return min(confidence, 95)

# === Smart Skip Filter ===
def should_skip_trade(rsi, macd_histogram, atr, price, confidence):
    atr_percent = atr / price

    if atr_percent < 0.005:
        return "ATR too low"

    if abs(macd_histogram) < 0.05:
        return "MACD too flat"

    if 48 < rsi < 52:
        return "RSI neutral zone"

    if confidence < 60:
        return "Low confidence"

    return None

# === Load Config ===
CONFIG_PATH = "smart_signal_config.json"
config = {
    "max_signals_per_run": 10,
    "volatility_threshold": 0.01,
    "confidence_threshold": 70,
    "skip_low_probability": True,
    "signal_tags": ["no-loss", "high-confidence"]
}
if os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH) as f:
        config.update(json.load(f))

# === Main Analyzer ===
def analyze_signals(data, symbol):
    try:
        closes = data["close"]
        highs = data["high"]
        lows = data["low"]
        dates = data["date"]

        atr = calculate_atr(highs, lows, closes)
        rsi = calculate_rsi(closes)
        macd, signal = calculate_macd(closes)
        latest_price = closes[-1]

        # Use latest indicators
        latest_rsi = rsi[-1]
        latest_macd = macd[-1]
        latest_signal = signal[-1]
        macd_hist = latest_macd - latest_signal

        confidence = calculate_confidence(latest_rsi, latest_macd, latest_signal, atr, latest_price)

        # === Skip logic (smart filtering) ===
        skip_reason = should_skip_trade(latest_rsi, macd_hist, atr, latest_price, confidence)
        if skip_reason:
            return None, f"⚠️ {symbol} skipped: {skip_reason}."

        breakout_level = max(highs[-3:])
        breakdown_level = min(lows[-3:])

        if latest_price > breakout_level and latest_macd > latest_signal and latest_rsi > 50:
            direction = "BUY"
            entry = round(latest_price, 2)
            target = round(entry + atr * 1.5, 2)
            stop = round(entry - atr * 0.75, 2)
        elif latest_price < breakdown_level and latest_macd < latest_signal and latest_rsi < 50:
            direction = "SELL"
            entry = round(latest_price, 2)
            target = round(entry - atr * 1.5, 2)
            stop = round(entry + atr * 0.75, 2)
        else:
            return None, f"⚠️ {symbol} skipped: No strong entry confirmation."

        insight = f"MACD: {round(latest_macd, 2)}, RSI: {round(latest_rsi, 2)}, ATR: {round(atr, 2)}"

        return {
            "symbol": symbol,
            "direction": direction,
            "entry": entry,
            "target": target,
            "stop": stop,
            "confidence": confidence,
            "insight": insight,
            "time": datetime.now().strftime("%H:%M %p")
        }, None

    except Exception as e:
        return None, f"[Strategy Error] {symbol}: {e}"
