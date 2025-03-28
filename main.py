from modules.data_loader import load_data
from modules.optimizations import objective_func
from modules.visualization import plot_strategy
from modules.metrics import calculate_metrics
import optuna

# Cargar datos
data = load_data("data/aapl_5m_train.csv")

# Optimizar
study = optuna.create_study(direction="maximize")
study.optimize(lambda trial: objective_func(trial, data), n_trials=100)

# Evaluar resultados
best_params = study.best_params
result = objective_func(optuna.trial.FixedTrial(best_params), data, return_full=True)

# Métricas
metrics = calculate_metrics(result["portfolio"], result["prices"], result["wins"], result["losses"])
for k, v in metrics.items():
    print(f"{k}: {v:.4f}")

# Visualización
plot_strategy(data, result["portfolio"])