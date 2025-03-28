def generate_signals(dataset, bb):
    dataset["RSI_BUY"] = dataset["RSI"] < 21 
    dataset["RSI_SELL"] = dataset["RSI"] > 80 

    dataset["BB_BUY"] = bb.bollinger_lband_indicator().astype(bool)
    dataset["BB_SELL"] = bb.bollinger_hband_indicator().astype(bool)

    dataset["MACD_BUY"] = False
    dataset["MACD_SELL"] = False

    macd = dataset["MACD"]
    macd_signal = dataset["macd_signal"]

    for i in range(1, len(dataset)):
        if macd.iloc[i] > macd_signal.iloc[i] and macd.iloc[i - 1] <= macd_signal.iloc[i - 1]:
            dataset.at[i, "MACD_BUY"] = True
        elif macd.iloc[i] < macd_signal.iloc[i] and macd.iloc[i - 1] >= macd_signal.iloc[i - 1]:
            dataset.at[i, "MACD_SELL"] = True

    return dataset.dropna()