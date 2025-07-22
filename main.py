import streamlit as st
import numpy as np
from utils import compute_pnl_heatmap, plot_heatmap

# === Streamlit App ===
st.set_page_config(layout="wide")


st.title("📊 Option PnL Heatmap Visualizer")

with st.sidebar:
    st.header("Input Parameters")

    S_min = st.number_input("Spot Price Min", value=80.0)
    S_max = st.number_input("Spot Price Max", value=120.0)
    vol_min = st.number_input("Volatility Min (%)", value=10.0)
    vol_max = st.number_input("Volatility Max (%)", value=50.0)
    resolution = st.slider("Grid Resolution", 5, 30, 10)

    K = st.number_input("Strike Price", value=100.0)
    T = st.number_input("Time to Maturity (Years)", value=1.0)
    r = st.number_input("Risk-Free Rate (%)", value=5.0) / 100
    entry_price = st.number_input("Option Entry Price", value=10.0)

S_range = np.linspace(S_min, S_max, resolution)
vol_range = np.linspace(vol_min, vol_max, resolution) / 100  # convert to decimal

# === Generate PnL Matrices ===
pnl_call = compute_pnl_heatmap(S_range, vol_range, K, T, r, entry_price, "call")
pnl_put = compute_pnl_heatmap(S_range, vol_range, K, T, r, entry_price, "put")

# === Plot Side-by-Side ===
col1, spacer, col2 = st.columns([5, 1, 5])
with col1:
    st.subheader("📈 Call Option PnL Heatmap")
    plot_heatmap(S_range, vol_range, pnl_call, "Call Option PnL Heatmap")

with col2:
    st.subheader("📉 Put Option PnL Heatmap")
    plot_heatmap(S_range, vol_range, pnl_put, "Put Option PnL Heatmap")