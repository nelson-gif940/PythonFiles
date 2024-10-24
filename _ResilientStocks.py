# test 
import pickle
import yfinance as yf
import csv

# *** First step, load all ticker from csv *** #

filename = "nasdaq.csv"
tickers = []
with open(filename, 'r') as csvfile:
  reader = csv.reader(csvfile)
  for row in reader:
    tickers.append(row[0])


# *** Second step, batch load data into pickle *** #

r1_start = "2001-03-01"
r1_end = "2001-11-01"

r2_start = "2007-12-01"
r2_end = "2009-06-01"

r3_start = "2020-02-01"
r3_end = "2020-04-01"

'''
dic_2020 = {}

with open("2020.pkl", "wb") as f:
  pickle.dump(dic_2020, f)

for i in range(0, 36):

  with open("2020.pkl", "rb") as f:
    dic_2020 = pickle.load(f)
    
  data = yf.download(tickers[i*100:(i+1)*100], r3_start, r3_end, period="1d")
  tickers_2 = tickers[i*100:(i+1)*100]
  for ticker in tickers_2:
    try: 
      if data["Close", ticker][0] < data["Close", ticker][-1]:
        print("Stock added 2020: " + ticker)
        percentage = data["Close", ticker][-1] / data["Close", ticker][0]
        dic_2020[ticker] = ["2020", round(percentage,2)]
    except:
      continue

  with open("2020.pkl", "wb") as f:
    pickle.dump(dic_2020, f)

  print("step _ done ___________> " + str(i))



dic_2008 = {}

with open("2008.pkl", "wb") as f:
  pickle.dump(dic_2008, f)

for i in range(0, 36):

  with open("2008.pkl", "rb") as f:
    dic_2008 = pickle.load(f)
  
  data = yf.download(tickers[i*100:(i+1)*100], r2_start, r2_end, period="1d")
  tickers_2 = tickers[i*100:(i+1)*100]
  for ticker in tickers_2:
    try: 
      if data["Close", ticker][0] < data["Close", ticker][-1]:
        print("Stock added 2008: " + ticker)
        percentage = data["Close", ticker][-1] / data["Close", ticker][0]
        dic_2008[ticker] = ["2008", round(percentage,2)]
    except:
      continue
  
  with open("2008.pkl", "wb") as f:
    pickle.dump(dic_2008, f)
  
  print("step _ done ___________> " + str(i))



dic_dotcom = {}

with open("dotcom.pkl", "wb") as f:
  pickle.dump(dic_dotcom, f)

for i in range(0, 36):

  with open("dotcom.pkl", "rb") as f:
    dic_dotcom = pickle.load(f)

  data = yf.download(tickers[i*100:(i+1)*100], r1_start, r1_end, period="1d")
  tickers_2 = tickers[i*100:(i+1)*100]
  for ticker in tickers_2:
    try: 
      if data["Close", ticker][0] < data["Close", ticker][-1]:
        print("Stock added dotcom: " + ticker)
        percentage = data["Close", ticker][-1] / data["Close", ticker][0]
        dic_dotcom[ticker] = ["2000",round(percentage,2)]
    except:
      continue

  with open("dotcom.pkl", "wb") as f:
    pickle.dump(dic_dotcom, f)

  print("step _ done ___________> " + str(i))

'''


with open("2020_done.pkl", "rb") as f:
  dic_2020 = pickle.load(f)

with open("2008_done.pkl", "rb") as f:
  dic_2008 = pickle.load(f)

with open("dotcom_done.pkl", "rb") as f:
  dic_2000 = pickle.load(f)

'''
dic_2008_2020 = {}
for keys,value in dic_2008.items():
  if keys in dic_2020.keys():
    dic_2008_2020[keys] = [value, dic_2020[keys]]

for key, value in dic_2008_2020.items():
  print(f"{key}: {value}")
  
'''
dic_all_r = {}

for keys,value in dic_2020.items():
  if keys in dic_2008.keys() and keys in dic_2000.keys():
    dic_all_r[keys] = [dic_2000[keys], dic_2008[keys], value]
    print("found one!")

for key, value in dic_all_r.items():
  print(f"{key}: {value}")
