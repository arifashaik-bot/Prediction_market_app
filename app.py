import streamlit as st
import plotly.express as px

from utils.data_loader import load_parquet_data
from utils.analytics import market_distribution, yes_price_trend, top_markets

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Prediction Market Intelligence",
    layout="wide"
)

st.title("📊 Prediction Market Intelligence Dashboard")
st.markdown(
    "High-performance analytics for prediction market datasets"
)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    return load_parquet_data("data")

df = load_data()

st.success(f"Loaded {len(df):,} records")

# Ensure required column exists
if "market_name" not in df.columns:
    df["market_name"] = df["market_ticker"]

# ---------------- SIDEBAR ----------------
st.sidebar.header("🔍 Filters")

markets = sorted(df["market_name"].unique())
selected_market = st.sidebar.selectbox(
    "Select Market",
    markets
)

# ---------------- MARKET DISTRIBUTION ----------------
st.subheader("📊 Market Distribution")

dist_df = market_distribution(df)

fig_bar = px.bar(
    dist_df.head(20),
    x="market_name",
    y="count",
    title="Top 20 Markets by Activity"
)

st.plotly_chart(fig_bar, use_container_width=True)

# ---------------- PIE CHART ----------------
st.subheader("🥧 Top 10 Markets Share")

top_df = top_markets(df)

fig_pie = px.pie(
    top_df,
    names="market_name",
    values="count",
    hole=0.4
)

st.plotly_chart(fig_pie, use_container_width=True)

# ---------------- PRICE TREND ----------------
st.subheader("📈 YES Price Trend")

trend_df = yes_price_trend(df, selected_market)

fig_line = px.line(
    trend_df,
    x="created_time",
    y="yes_price",
    title=f"YES Price Trend — {selected_market}"
)

st.plotly_chart(fig_line, use_container_width=True)

# ---------------- TABLE: RECENT TRADES ----------------
st.subheader("📋 Recent Trades")

recent_trades = (
    trend_df
    .sort_values("created_time", ascending=False)
    .head(50)
)

st.dataframe(
    recent_trades[
        [
            "created_time",
            "yes_price",
            "no_price",
            "taker_side",
            "market_ticker"
        ]
    ],
    use_container_width=True
)

# ---------------- RAW DATA ----------------
st.subheader("🗂 Raw Data Preview")

with st.expander("View raw dataset"):
    st.dataframe(df.head(100), use_container_width=True)