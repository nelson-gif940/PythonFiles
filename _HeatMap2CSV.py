# ------------------------------------------------------------- #
# ----------------------- HEAT MAP ---------------------------- #
# ------------------------------------------------------------- #

# ------------------------------------------------------------- #
# ---------- export data heatmap to xlxs ---------------------- #

# Libraries ------------------------- /

import pandas as pd
import numpy as np
import yfinance as yf
import pandas_ta as ta
from openpyxl import Workbook
from ta.momentum import StochasticOscillator

# Array creation -------------------- /

currency_pairs = ["EURUSD=X","GBPUSD=X","USDCHF=X","AUDUSD=X","CADUSD=X","USDJPY=X","GC=F","BZ=F","BTC-USD"]

indicators = []

# Indicator ------------------------- /

for k in range(len(currency_pairs)):
  # Name

  array_indicator=[]
  ticker=currency_pairs[k]
  stock = yf.Ticker(ticker)
  historical_data = stock.history(period="1y")
  array_indicator.append(currency_pairs[k])

  # Last close

  array_indicator.append(historical_data["Close"][-1])

  # Moving Average

  sma_60 = historical_data["Close"].rolling(60).mean()
  sma_144 = historical_data["Close"].rolling(144).mean()
  array_indicator.append(1-(sma_60.iloc[-1]/historical_data["Close"][-1]))
  array_indicator.append(1-(sma_144.iloc[-1]/historical_data["Close"][-1]))

  # Rsi

  historical_data['RSI'] = ta.rsi(historical_data['Close'], length=14)
  array_indicator.append(historical_data['RSI'].iloc[-1])

  # Stoch

  stoch = StochasticOscillator(high=historical_data["High"], low=historical_data["Low"], close=data["Close"], window=14)
  historical_data["%K"] = stoch.stoch()
  historical_data["%D"] = stoch.stoch_signal()
  array_indicator.apppend(historical_data["%K"].iloc[-1])
  array_indicator.apppend(historical_data["%D"].iloc[-1])
  print(historical_data["%K"].iloc(-1))

  # Append to array

  indicators.append(array_indicator)

# Export to csv -------------------- /

with open("data.csv", "w", newline="") as f:
  writer = csv.writer(f)
  for row in indicators:
      writer.writerow(row)
f.close()

# Export to xlsx -------------------- /

df = pd.read_csv('data.csv')
df.to_excel('heatmap.xlsx', index=False)

