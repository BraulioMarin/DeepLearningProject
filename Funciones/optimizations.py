import ta

def objective_func(trial, data,return_full=False):
    # Parámetros RSI
    rsi_window = trial.suggest_int("rsi_window", 10, 100)
    rsi_lower = trial.suggest_int("rsi_lower", 5, 35)
    rsi_upper = trial.suggest_int("rsi_upper", 65, 95)

    # Bollinger Bands
    bb_window = trial.suggest_int("bb_window", 10, 100)
    bb_window_dev = trial.suggest_int("bb_window_dev", 1, 3)

    # MACD
    slow_window = trial.suggest_int("window_slow", 13, 30)
    fast_window = trial.suggest_int("window_fast", 1, 12)
    window_signal = trial.suggest_int("window_sign", 1, 50)

    # Stop loss, take profit, cantidad de acciones
    stop_loss = trial.suggest_float("stop_loss", 0.01, 0.2)
    take_profit = trial.suggest_float("take_profit", 0.01, 0.2)
    n_shares = trial.suggest_categorical("n_shares", [1000, 1200, 3000, 5000,7000, 8000])

    # Dataset y cálculos de indicadores
    dataset = data.copy()
    dataset["RSI"] = ta.momentum.RSIIndicator(dataset.Close, window=rsi_window).rsi()
    bb = ta.volatility.BollingerBands(dataset.Close, window=bb_window, window_dev=bb_window_dev)
    dataset["BB_MAVG"] = bb.bollinger_mavg()
    dataset["BB_BUY"] = bb.bollinger_lband_indicator().astype(bool)
    dataset["BB_SELL"] = bb.bollinger_hband_indicator().astype(bool)

    macd = ta.trend.MACD(data.Close, window_slow=slow_window, window_fast=fast_window, window_sign=window_signal)
    dataset["MACD"] = macd.macd()
    dataset["MACD_SIGNAL"] = macd.macd_signal()
    dataset["MACD_BUY"] = False
    dataset["MACD_SELL"] = False

    # Señales RSI
    dataset["RSI_BUY"] = dataset["RSI"] < rsi_lower
    dataset["RSI_SELL"] = dataset["RSI"] > rsi_upper

    # Señales MACD (cruce)
    for i in range(1, len(dataset)):
        if dataset["MACD"].iloc[i] > dataset["MACD_SIGNAL"].iloc[i] and dataset["MACD"].iloc[i - 1] <= dataset["MACD_SIGNAL"].iloc[i - 1]:
            dataset.at[dataset.index[i], "MACD_BUY"] = True
        elif dataset["MACD"].iloc[i] < dataset["MACD_SIGNAL"].iloc[i] and dataset["MACD"].iloc[i - 1] >= dataset["MACD_SIGNAL"].iloc[i - 1]:
            dataset.at[dataset.index[i], "MACD_SELL"] = True

    dataset = dataset.dropna()

    capital = 1_000_000
    com = 0.00125
    portfolio_value = [capital]
    portfolio_dates = [dataset.index[0]]
    wins = 0
    losses = 0

    active_long_positions = None
    active_short_positions = None

    for i, row in dataset.iterrows():
        price = row.Close

        # Cierre de posición larga
        if active_long_positions:
            entry = active_long_positions["opened_at"]
            if price <= active_long_positions["stop_loss"] or price >= active_long_positions["take_profit"]:
                pnl = price * n_shares * (1 - com)
                capital += pnl
                if price > entry:
                    wins += 1
                else:
                    losses += 1
                active_long_positions = None

        # Cierre de posición corta
        if active_short_positions:
            entry = active_short_positions["opened_at"]
            if price >= active_short_positions["stop_loss"] or price <= active_short_positions["take_profit"]:
                pnl = (entry - price) * n_shares * (1- com)
                capital += pnl
                if price < entry:
                    wins += 1
                else:
                    losses += 1
                active_short_positions = None

        # Apertura de posición larga
        if (row.RSI_BUY + row.BB_BUY + row.MACD_BUY) >= 2 and not active_long_positions and not active_short_positions:
            cost = price * n_shares * (1 + com)
            if capital >= cost:
                capital -= cost
                active_long_positions = {
                    "datetime": row.Datetime,
                    "opened_at": price,
                    "take_profit": price * (1 + take_profit),
                    "stop_loss": price * (1 - stop_loss)
                }

        # Apertura de posición corta
        if (row.RSI_SELL + row.BB_SELL + row.MACD_SELL) >= 2 and not active_short_positions and not active_long_positions:
            margin = price * n_shares * com
            if capital >= margin:
                capital -= margin
                active_short_positions = {
                    "datetime": row.Datetime,
                    "opened_at": price,
                    "take_profit": price * (1 - take_profit),
                    "stop_loss": price * (1 + stop_loss)
                }

        # Valor actual del portafolio
        long_value = row.Close * n_shares if active_long_positions else 0
        short_value = (active_short_positions["opened_at"] - price) * n_shares if active_short_positions else 0
        portfolio_value.append(capital + long_value + short_value)
        portfolio_dates.append(row.name)
        
    if return_full:
        return {
            "portfolio": portfolio_value,
            "wins": wins,
            "losses": losses,
            "prices": dataset.Close
        }

    
    return portfolio_value[-1]