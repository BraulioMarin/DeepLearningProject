import ta

def add_indicators(data, rsi_window=67, bb_window=75, bb_dev=1, macd_fast=11, macd_slow=20, macd_signal=21):
    dataset = data.copy()
    rsi = ta.momentum.RSIIndicator(dataset.Close, window=rsi_window)
    bb = ta.volatility.BollingerBands(dataset.Close, window=bb_window, window_dev=bb_dev)
    macd = ta.trend.MACD(dataset.Close, window_slow=macd_slow, window_fast=macd_fast, window_sign=macd_signal)

    dataset["RSI"] = rsi.rsi()
    dataset["BB"] = bb.bollinger_mavg()
    dataset["macd_signal"] = macd.macd_signal()
    dataset["MACD"] = macd.macd()

    return dataset, bb