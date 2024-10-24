import yfinance as yf
import numpy as np
import pandas as pd

class compute:
  def __init__(self) -> None:
    pass
    
  def pct(self,list):
    output = []
    for i in range(1,len(list)):
      output.append((list[i]-list[i-1])/list[i-1])
    return output

  def var(self, list):
    output = 0
    mean_ = np.mean(list)
    for i in range(len(list)):
      output += (list[i]-mean_)**2
    return output / len(list)

  def cov(self, list_1, list_2):
    output = 0
    mean_1 = np.mean(list_1)
    mean_2 = np.mean(list_2)
    for i in range(len(list_1)):
      output += (list_1[i]-mean_1)*(list_2[i]-mean_2)
    return output / (len(list_1))

  def standard_dev(self, list1):
    mean_ = np.mean(list1)
    squared_dev = [pow(x - mean_, 2) for x in list1]
    var = np.mean(squared_dev)
    std = np.sqrt(var)
    return std

  def total_return(self, list):
    return list[-1]/list[0]

  def sharpe_ratio(self, total_return, std, risk_free_rate):
    annualized_std = std * np.sqrt(252)
    sharpe_ratio = ( total_return - risk_free_rate) / annualized_std
    return sharpe_ratio

  def beta(self, list_1, benchmark):
    beta = self.cov(list_1, benchmark) / self.var(benchmark)
    return beta

  def ortho(self, list_of_stock, list_1, benchmark):
    list_1.append(benchmark)
    list_of_stock.append("Benchmark")
    cov_dic = {}
    mean_ortho = {}
    for i in range(len(list_1)):
      cov_list = []
      for k in range(len(list_1)):
        cov = self.cov(list_1[i], list_1[k]) / (self.standard_dev(list_1[i]) * self.standard_dev(list_1[k]))
        cov_list.append([list_of_stock[k],cov])
      cov_dic[list_of_stock[i]] = cov_list
      mean_ortho[list_of_stock[i]] = np.mean([cov_list[k][1] for k in range(len(cov_list))]) - 1/len(cov_list)
      
    return cov_dic, mean_ortho

  def standard_dev_port(self,pct_return, list_of_weight):
    std = 0
    for k in range(len(list_of_weight)):
      for i in range(k+1,len(list_of_weight)):
        std_1 = self.standard_dev(pct_return[i])
        std_2 = self.standard_dev(pct_return[k])
        w_1 = list_of_weight[i]
        w_2 = list_of_weight[k]
        cov = self.cov(pct_return[i], pct_return[k])
        std += w_1**2 * std_1**2 + w_2**2 * std_2**2 + 2*w_1*w_2*cov

    return np.sqrt(std)
        

class get_data:
  
  def __init__(self) -> None:
    pass

  def ddata(self, list, start, end):
    array = []
    for i in range(len(list)):
      array.append(yf.download(list_of_stocks[i],start_date, end_date))
    return array
  

def download_data(list_of_stocks, benchmark, start_date, end_date):
  ''' 
  Download the data from yfinance for the list of stock and benchmark data
  '''
  data_stock = []
  for i in range(len(list_of_stocks)):
    data_stock.append(yf.download(list_of_stocks[i],start_date, end_date))
  benchmark_data = yf.download(benchmark,start_date, end_date)

  return data_stock, benchmark_data


# *** test

dic = {}

list_of_stocks = ["AMD","GNE","QCOM","NVDA","MPX","TSRI","CCLD","SOTK"] #needs to be sorted
list_of_weight = [0.125]*8
data_stock, benchmark_data = download_data(list_of_stocks, "SPY", "2023-05-01", "2024-06-01")

return_pct = [compute().pct(data_stock[k]["Close"]) for k in range(len(data_stock))]
return_benchmark = compute().pct(benchmark_data["Close"])

std_stocks = [compute().standard_dev(return_pct[k]) for k in range(len(return_pct))]
std_benchmark = compute().standard_dev(return_benchmark)

std_portfolio = compute().standard_dev_port(return_pct, list_of_weight)
dic["Standard Deviation"] = round(std_portfolio,2)

total_return = np.dot([compute().total_return(data_stock[k]["Close"]) for k in range(len(data_stock))], list_of_weight)
sharpe_ratio = compute().sharpe_ratio(total_return, std_portfolio, 0.046)
dic["Sharpe Ratio"] = round(sharpe_ratio,2)

betas = [compute().beta(return_pct[k], return_benchmark) for k in range(len(return_pct))]
portfolio_beta = np.dot(betas, list_of_weight)
dic["Portfolio Beta"] = round(portfolio_beta,2)
dic["Stock betas"] = betas

return_portfolio = [np.dot([item[k] for item in return_pct],list_of_weight) for k in range(len(return_pct[0]))]
correlation = compute().cov(return_portfolio, return_benchmark) / (std_portfolio * std_benchmark)
dic["Correlation"] = round(correlation,2)

ortho, mean_ortho = compute().ortho(list_of_stocks, return_pct, return_benchmark)
dic["Ortho"] = ortho
dic["Mean Ortho"] = mean_ortho

print("_______")
print("Results:")
print("_______")

for key, value in dic.items():
  if key == "Ortho":
    for key, value in dic[key].items():
      print(f"{key}: {value}")
      print(" ________________________ ")
  else:
    print(f"{key}: {value}")
    print(" -- / -- ")

