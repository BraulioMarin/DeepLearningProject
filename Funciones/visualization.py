import matplotlib.pyplot as plt

def plot_strategy(data, portfolio):
    fig, ax = plt.subplots(1, 1, figsize=(14, 6))
    
    # Graficar el valor del portafolio
    ax.plot(portfolio, label="Portfolio Value", color="C0", linewidth=2)
    ax.set_ylabel("Valor del Portafolio", color="C0")
    ax.tick_params(axis='y', labelcolor="C0")
    
    # Graficar el precio del activo en el eje derecho
    ax2 = ax.twinx()
    ax2.plot(data.Close, label="Precio del Activo", color="C1", linestyle="--")
    ax2.set_ylabel("Precio del Activo", color="C1")
    ax2.tick_params(axis='y', labelcolor="C1")
    
    # Títulos y leyenda
    plt.title("Estrategia de Trading: Portafolio vs Precio del Activo")
    fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.9))
    plt.grid(True)
    plt.tight_layout()
    plt.show()
