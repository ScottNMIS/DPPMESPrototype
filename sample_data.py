import pandas as pd
import numpy as np

def get_large_sample_data():
    np.random.seed(42)
    data = {
        'Company': [f'Company {i}' for i in range(1, 101)],
        'Value X': np.random.randint(100, 1000, 100),
        'Value Y': np.random.randint(200, 800, 100),
        'Location': ['City A', 'City B', 'City C', 'City D', 'City E'] * 20,
        'Latitude': np.random.uniform(-90, 90, 100),
        'Longitude': np.random.uniform(-180, 180, 100),
        'Date': pd.date_range(start='1/1/2023', periods=100, freq='D')
    }
    return pd.DataFrame(data)
