import csv
import yfinance as yf
import pickle
import pandas as pd


def import_csv_to_list(filename):
  data = []
  try:
    with open(filename, 'r') as csvfile:
      reader = csv.reader(csvfile)
      for row in reader:
        data.append(row[0])
    return data
  except FileNotFoundError:
    print(f"Error: File not found - {filename}")
  except Exception as e:
    print(f"Error: An unexpected error occurred - {e}")

'''
variable = {}
with open("stock_data.pkl", "wb") as f:
  pickle.dump(variable, f)

data = "nasdaq.csv"
tickers = import_csv_to_list(data)




for i in range(0,36):
  print("___________________________ step :" + i)
  if i+100 < len(tickers):
    stock_data = yf.download(tickers[i*100:(i+1)*100]+["SPY"], start="2023-06-01", end="2024-06-01")
    stock_data = stock_data["Close"]
    corr_ = stock_data.corr()
    with open("stock_data.pkl", "rb") as f:
      variable = pickle.load(f)
    variable[i] = corr_["SPY"]
    with open("stock_data.pkl", "wb") as f:
      pickle.dump(variable, f)
    print(i)
  else:
    stock_data = yf.download(tickers[i*100:(i+1)*100]+["SPY"], start="2023-06-01", end="2024-06-01")
    stock_data = stock_data["Close"]
    corr_ = stock_data.corr()
    with open("stock_data.pkl", "rb") as f:
      variable = pickle.load(f)
    variable[i] = corr_
    with open("stock_data.pkl", "wb") as f:
      pickle.dump(variable, f)


'''

with open("stock_data.pkl", "rb") as f:
  variable = pickle.load(f)

print(variable[1])

dic = {}
for i in range(len(variable)):
  for item, keys in variable[i].items():
    if item not in dic:
      dic[item] = keys

lowest_stock = {}
for item, key in dic.items():
  if key < -0.90:
    lowest_stock[item] = key

for key, value in lowest_stock.items():
  print(f"{key}: {value}")