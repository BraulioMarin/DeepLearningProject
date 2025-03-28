import numpy as np

def calculate_metrics(portfolio, prices, wins, losses):
    returns = np.diff(portfolio) / portfolio[:-1]
    if len(returns) == 0:
        return {
            "Sharpe Ratio": 0,
            "Sortino Ratio": 0,
            "Calmar Ratio": 0,
            "Win Rate": 0,
        }

    # Tasa libre de riesgo diaria (10% anual)
    risk_free_rate = 0.10 / 19656
    excess_returns = returns - risk_free_rate

    # Sharpe ratio
    sharpe = (
        np.mean(excess_returns) / np.std(returns) * np.sqrt(19656)
        if np.std(returns) > 0 else 0
    )

    # Sortino ratio
    downside = excess_returns[excess_returns < 0]
    sortino = (
        np.mean(excess_returns) / np.std(downside) * np.sqrt(19656)
        if len(downside) > 0 and np.std(downside) > 0 else 0
    )

    # Calmar ratio
    cumulative_return = portfolio[-1] / portfolio[0] - 1
    drawdown = portfolio / np.maximum.accumulate(portfolio) - 1
    max_drawdown = np.min(drawdown)
    calmar = (cumulative_return) / abs(max_drawdown) if max_drawdown < 0 else 0

    # Win rate
    total_trades = wins + losses
    win_rate = wins / total_trades if total_trades > 0 else 0

    return {
        "Sharpe Ratio": sharpe,
        "Sortino Ratio": sortino,
        "Calmar Ratio": calmar,
        "Win Rate": win_rate
    }