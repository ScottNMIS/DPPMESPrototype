import pandas as pd
import numpy as np
import datetime

def generate_sample_data():
    np.random.seed(0)
    data = {
        "Date": pd.date_range(start="2023-01-01", periods=100),
        "Value_X": np.random.randn(100).cumsum(),
        "Value_Y": np.random.randn(100).cumsum(),
        "Value_Z": np.random.randn(100).cumsum(),
        "Value_L": np.random.randn(100).cumsum(),
        "Latitude": np.random.uniform(-90, 90, 100),
        "Longitude": np.random.uniform(-180, 180, 100),
    }
    df = pd.DataFrame(data)
    return df

def get_data():
    df = generate_sample_data()
    return df
