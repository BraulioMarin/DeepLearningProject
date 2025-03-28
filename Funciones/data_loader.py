import pandas as pd

def load_data(path):
    data = pd.read_csv('/Users/Usuario/Documents/10 SEMESTRE/Trading/003_deeplearning/data/aapl_5m_train.csv').dropna()
    return data