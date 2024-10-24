import numpy as np
import yfinance as yf
import pandas as pd

tickers_list = ["BTC-USD", "ETH-USD", "USDT-USD", "BNB-USD", "SOL-USD", "STETH-USD", "USDC-USD", "XRP-USD", "DOGE-USD", "TON11419-USD", "ADA-USD", "AVAX-USD", "SHIB-USD", "WBTC-USD", "DOT_USD", "WTRX-USD", "TRX-USD", "BCH-USD", "LINK-USD","NEAR-USD"]

data = yf.download(tickers_list, period="1d", start="2022-01-01", end="2024-05-22")
df = pd.DataFrame(data)

data_pct = df["Close"].pct_change()
print(data_pct)

corr = data_pct.corr(method='pearson', min_periods=1, numeric_only=False)
print(corr.iloc[4])




