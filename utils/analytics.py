import pandas as pd

def market_distribution(df: pd.DataFrame):
    if "market_name" not in df.columns:
        df["market_name"] = df["market_ticker"]

    return df["market_name"].value_counts().reset_index(
        name="count"
    ).rename(columns={"index": "market_name"})


def yes_price_trend(df: pd.DataFrame, market_name: str):
    filtered = df[df["market_name"] == market_name].copy()
    filtered["created_time"] = pd.to_datetime(filtered["created_time"])

    return filtered.sort_values("created_time")


def top_markets(df: pd.DataFrame, n=10):
    return (
        df["market_name"]
        .value_counts()
        .head(n)
        .reset_index(name="count")
        .rename(columns={"index": "market_name"})
    )