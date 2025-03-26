import matplotlib.pyplot as plt

def simular_estrategia(dataset):
    capital = 1_000_000
    com = 0.125 / 100

    portfolio_value = [capital]

    stop_loss = 0.05
    take_profit = 0.05
    n_shares = 1000

    wins = 0
    losses = 0

    active_long_positions = None
    active_short_positions = None

    for i, row in dataset.iterrows():
        # Close long positions
        if active_long_positions:
            # Closed by stop loss
            if row.Close < active_long_positions["stop_loss"]:
                pnl = row.Close * n_shares * (1 - com)
                capital += pnl
                active_long_positions = None

        if active_long_positions:
            # Closed by take profit
            if row.Close > active_long_positions["take_profit"]:
                pnl = row.Close * n_shares * (1 - com)
                capital += pnl
                active_long_positions = None

        # Close short positions
        if active_short_positions:
            # Closed by stop loss
            if row.Close > active_short_positions["stop_loss"]:
                entrada = active_short_positions["opened_at"]
                salida = row.Close
                pnl = (entrada - salida) * n_shares * (1 - com)
                capital += pnl
                active_short_positions = None

        if active_short_positions:
            # Closed by take profit
            if row.Close < active_short_positions["take_profit"]:
                entrada = active_short_positions["opened_at"]
                salida = row.Close
                pnl = (entrada - salida) * n_shares * (1 - com)
                capital += pnl
                active_short_positions = None

        # Open Long positions
        if row.RSI_BUY and active_long_positions is None:
            cost = row.Close * n_shares * (1 + com)
            if capital > cost:
                capital -= cost
                active_long_positions = {
                    "datetime": row.Datetime,
                    "opened_at": row.Close,
                    "take_profit": row.Close * (1 + take_profit),
                    "stop_loss": row.Close * (1 - stop_loss)
                }

        # Open short positions
        if row.RSI_SELL and active_short_positions is None:
            cost = row.Close * n_shares * com
            if capital > cost:
                capital -= cost
                active_short_positions = {
                    "datetime": row.Datetime,
                    "opened_at": row.Close,
                    "take_profit": row.Close * (1 - take_profit),
                    "stop_loss": row.Close * (1 + stop_loss)
                }


        # Calculate long positions value
        long_value = 0
        if active_long_positions:
            long_value = row.Close * n_shares

        # Calculate short positions value
        short_value = 0
        if active_short_positions:
            entrada = active_short_positions["opened_at"]
            short_value = (entrada - row.Close) * n_shares

            # Calculate portafolio value

        # Add portfolio value
        portfolio_value.append(capital + long_value + short_value)

    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    ax.plot(portfolio_value, label="Portfolio Value")
    ax.legend()
    ax2 = ax.twinx()
    ax2.plot(dataset.Close, c="C1")

    plt.show()

    return portfolio_value