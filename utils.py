import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm
import streamlit as st


def bs_price(S, K, T, r, sigma, option_type="call"):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == "call":
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == "put":
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("Invalid option type.")

# print(bs_price(S=100, K=100, T=1, r=0.05, sigma=0.2, option_type="call"))

# === Compute PnL Matrix ===
def compute_pnl_heatmap(S_range, vol_range, K, T, r, entry_price, option_type):
    pnl_matrix = []
    for sigma in vol_range:
        row = []
        for S in S_range:
            price = bs_price(S, K, T, r, sigma, option_type)
            pnl = price - entry_price
            row.append(pnl)
        pnl_matrix.append(row)
    return np.array(pnl_matrix)

# === Heatmap Plot ===
def plot_heatmap(x_range, y_range, data, title, cmap="RdYlGn"):
    fig, ax = plt.subplots(figsize=(10, 8))

    # Main heatmap
    sns.heatmap(data,
                cmap=cmap,
                xticklabels=np.round(x_range, 2),
                yticklabels=np.round(y_range * 100, 2),
                annot=True if len(x_range) <= 20 else False,
                fmt=".1f",
                linewidths=0.3,
                linecolor="white",
                cbar_kws={"shrink": 0.8},
                ax=ax)

    # Breakeven contour
    X, Y = np.meshgrid(x_range, y_range * 100)  # y in percent for display
    contour = ax.contour(X, Y, data, levels=[0], colors='black', linewidths=2, linestyles="--")
    ax.clabel(contour, fmt="Breakeven", fontsize=10, inline=True)

    # Labels and title
    ax.set_title(title, fontsize=14)
    ax.set_xlabel("Spot Price", fontsize=12)
    ax.set_ylabel("Volatility (%)", fontsize=12)
    ax.tick_params(axis='x', labelrotation=45)

    st.pyplot(fig)


