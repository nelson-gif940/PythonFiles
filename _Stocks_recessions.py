import csv
import yfinance as yf
import pickle


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

############################################################

def intersection_of_dicts_all_values(dicts):
  
  if not dicts:
    return {}  

  key_sets = [set(d.keys()) for d in dicts]

  common_keys = set.intersection(*key_sets)

  intersection_dict = {}
  for key in common_keys:
    values = []
    for d in dicts:
      if key in d: 
        values.append(d[key])
    intersection_dict[key] = values

  return intersection_dict

############################################################

def download_specific_prices(tickers, date1,date2):
  price_differences = {}
  price = yf.download(tickers, start=date1, end=date2)
  for ticker in tickers:
    try:
      price1_ticker = price.loc[ticker, str(date1)]["Close"]
      price2_ticker = price.loc[ticker, str(date2)]["Close"]

      # Check if data exists for both dates
      if price1_ticker is not None and price2_ticker is not None:
        price_difference = price2_ticker - price1_ticker
        if price_difference > 0:
          price_differences[ticker] = price_difference
      else:
        print(f"Incomplete data for {ticker} (missing date).")
    except (KeyError, ValueError) as e:
      print(f"Error: An error occurred while retrieving data for {ticker} - {e}")
      price_differences[ticker] = None  # Mark ticker with error

  return price_differences

############################################################

# GET DATA

data = "nasdaq.csv"
tickers = import_csv_to_list(data)

variable = {}
with open("stock_data.pkl", "wb") as f:
  pickle.dump(variable, f)
  
for i in range(0,36):
  if i+100 < len(tickers):
    with open("stock_data.pkl", "rb") as f:
      variable = pickle.load(f)
    variable[i] = yf.download(tickers[i*100:(i+1)*100])
    with open("stock_data.pkl", "wb") as f:
      pickle.dump(variable, f)
    print(i)
  else:
    with open("stock_data.pkl", "rb") as f:
      variable = pickle.load(f)
    variable[i] = yf.download(tickers[i*100:len(tickers)])
    with open("stock_data.pkl", "wb") as f:
      pickle.dump(variable, f)


'''

# RECESSIONS DATE

r1_start = "2001-03-01"
r1_end = "2001-11-01"

r2_start = "2007-12-01"
r2_end = "2009-06-01"


r3_start = "2020-02-01"
r3_end = "2020-04-01"

# INTERSECTION

r1_data = download_specific_prices(tickers, r1_start, r1_end)
r2_data = download_specific_prices(tickers, r2_start, r2_end)
r3_data = download_specific_prices(tickers, r3_start, r3_end)

print(r2_data)

common_increased_stocks = intersection_of_dicts_all_values([r1_data, r2_data, r3_data])

print("Stocks with price increases in all datasets:")
for stock in common_increased_stocks:
  print(stock)

with open("stocks", "w", newline="") as csvfile:
  writer = csv.writer(csvfile)
  writer.writerow(["Stock Ticker"])  # Write header row

  # Write each stock ticker to the CSV file
  for stock in common_increased_stocks:
    writer.writerow([stock])

    '''