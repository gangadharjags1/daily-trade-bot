import numpy as np

def calculate_rsi(prices, period=14):
    prices = np.array(prices)
    deltas = np.diff(prices)
    seed = deltas[:period]
    up = seed[seed > 0].sum() / period
    down = -seed[seed < 0].sum() / period
    rs = up / down if down != 0 else 0
    rsi = np.zeros_like(prices)
    rsi[:period] = 100. - 100. / (1. + rs)

    for i in range(period, len(prices)):
        delta = deltas[i - 1]
        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up * (period - 1) + upval) / period
        down = (down * (period - 1) + downval) / period
        rs = up / down if down != 0 else 0
        rsi[i] = 100. - 100. / (1. + rs)

    return rsi

def calculate_macd(prices, slow=26, fast=12, signal=9):
    prices = np.array(prices)
    exp1 = np.convolve(prices, np.ones(fast)/fast, mode='valid')
    exp2 = np.convolve(prices, np.ones(slow)/slow, mode='valid')
    min_len = min(len(exp1), len(exp2))
    macd_line = exp1[-min_len:] - exp2[-min_len:]
    signal_line = np.convolve(macd_line, np.ones(signal)/signal, mode='valid')
    # Pad to match length
    macd_line = macd_line[-len(signal_line):]
    return macd_line, signal_line

def calculate_atr(highs, lows, closes, period=14):
    highs = np.array(highs)
    lows = np.array(lows)
    closes = np.array(closes)

    tr = np.maximum(highs[1:], closes[:-1]) - np.minimum(lows[1:], closes[:-1])
    atr = np.mean(tr[-period:])
    return atr
