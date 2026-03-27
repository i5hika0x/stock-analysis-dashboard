# ===== INDIAN STOCK ANALYSIS PROJECT =====

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

print("===== INDIAN STOCK MARKET ANALYSIS =====")

# Step 1: Stocks list (including NIFTY 50)
stocks = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "^NSEI"]

# Step 2: Download data
data = yf.download(stocks, start="2023-01-01", end="2024-12-31")['Close']

# Step 3: Normalize for comparison
normalized = data / data.iloc[0]

# Step 4: Plot comparison
plt.figure(figsize=(12,6))
for stock in stocks:
    if stock == "^NSEI":
        plt.plot(normalized[stock], label="NIFTY 50", linestyle='dashed')
    else:
        plt.plot(normalized[stock], label=stock)

plt.title("Indian Stock Comparison vs NIFTY 50")
plt.xlabel("Date")
plt.ylabel("Growth")
plt.legend()
plt.show()

# Step 5: Calculate returns
returns = (data.iloc[-1] - data.iloc[0]) / data.iloc[0]

print("\n===== STOCK RETURNS =====")
for stock in returns.index:
    name = "NIFTY 50" if stock == "^NSEI" else stock
    print(f"{name}: {returns[stock]*100:.2f}%")

# Step 6: Ranking
print("\n===== RANKING =====")
sorted_returns = returns.sort_values(ascending=False)
for stock in sorted_returns.index:
    name = "NIFTY 50" if stock == "^NSEI" else stock
    print(f"{name}: {sorted_returns[stock]*100:.2f}%")

# Step 7: Best stock
best_stock = returns.idxmax()
print(f"\nBest Performing Stock: {best_stock}")

# Step 8: Decision
best_data = yf.download(best_stock, start="2023-01-01", end="2024-12-31")

best_data['MA7'] = best_data['Close'].rolling(7).mean()
best_data['MA30'] = best_data['Close'].rolling(30).mean()

if best_data['MA7'].iloc[-1] > best_data['MA30'].iloc[-1]:
    decision = "BUY"
else:
    decision = "HOLD"

print(f"Suggested Action for {best_stock}: {decision}")