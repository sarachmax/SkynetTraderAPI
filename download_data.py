import pandas as pd 
import requests
from io import StringIO 
import config


account_no = config.account_no
headers = {"X-API-KEY": config.api_key}

symbol = str(input("Symbol : "))
timeframe = str(input("Timeframe (5,15,60,D) : "))
start_time = str(input("StartDate 'YYYY-MM-DD': "))
end_time = str(input("EndDate 'YYYY-MM-DD': "))

req_hist_data_url = "https://api.skynetsystems.co.th/api/v1/data/candlestick/000/"+account_no+"?symbol="+symbol+"&timeframe="+timeframe+"&startTime="+start_time+"&endTime="+end_time

respones_hist = requests.get(req_hist_data_url, headers=headers)
if respones_hist.status_code == 200 : 
    print("Download data success !")
else : 
    print(r)
    print("Connection error, please try again")
    
df = pd.read_csv(StringIO(respones_hist.text),
                        names=['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'OI'],
                        index_col='Date', parse_dates=True)

filename = ""
foldername = "Data/"
if timeframe == "D":
    file_name = foldername + symbol + "_1" + timeframe + ".csv"
else : 
    file_name = foldername + symbol + "_" + timeframe + "M.csv"

df.to_csv(file_name)    