import pandas as pd
from pathlib import Path

def load_parquet_data(data_dir: str):
    data_path = Path(data_dir)
    files = list(data_path.glob("*.parquet"))

    if not files:
        raise FileNotFoundError("No parquet files found in data directory")

    df_list = [pd.read_parquet(file) for file in files]
    df = pd.concat(df_list, ignore_index=True)

    return df