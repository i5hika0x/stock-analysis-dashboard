import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Indian Stock Market Dashboard")

# Select stocks
stocks = st.multiselect(
    "Select Stocks",
    ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS"],
    default=["RELIANCE.NS", "TCS.NS"]
)

# Include NIFTY
if st.checkbox("Include NIFTY 50"):
    stocks.append("^NSEI")

# Load data
data = yf.download(stocks, start="2023-01-01", end="2024-12-31")['Close']

# Normalize
normalized = data / data.iloc[0]

# Plot graph
st.subheader("📈 Stock Comparison")
fig, ax = plt.subplots()

for stock in stocks:
    if stock == "^NSEI":
        ax.plot(normalized[stock], label="NIFTY 50", linestyle='dashed')
    else:
        ax.plot(normalized[stock], label=stock)

ax.legend()
st.pyplot(fig)

# Returns
returns = (data.iloc[-1] - data.iloc[0]) / data.iloc[0]

st.subheader("📊 Returns (%)")
st.write((returns * 100).sort_values(ascending=False))

# Best stock
best_stock = returns.idxmax()
st.success(f"🏆 Best Performing Stock: {best_stock}")

# Decision logic
best_data = yf.download(best_stock, start="2023-01-01", end="2024-12-31")
best_data['MA7'] = best_data['Close'].rolling(7).mean()
best_data['MA30'] = best_data['Close'].rolling(30).mean()

if best_data['MA7'].iloc[-1] > best_data['MA30'].iloc[-1]:
    decision = "BUY"
else:
    decision = "HOLD"

st.info(f"📌 Suggested Action for {best_stock}: {decision}")