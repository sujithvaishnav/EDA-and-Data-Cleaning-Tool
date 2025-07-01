import pandas as pd

def load_data(file):
    try:
        return pd.read_csv(file)
    except Exception as e:
        print(f"Error loading file: {e}")
        return None
