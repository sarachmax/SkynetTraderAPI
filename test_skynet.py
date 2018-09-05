# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 10:47:30 2018

@author: SarachErudite
"""

import requests 
import json 
import pandas as pd 
from io import StringIO
import pika 

account_no = "1053038-1" 
headers = {"X-API-KEY": "4269B42F4E5B1431FC58801B1066FE47"}

# test portfolio info 
req_port_info_url = 'https://api.skynetsystems.co.th/api/v1/account/000/'+account_no

response = requests.get(req_port_info_url, headers=headers) 
portfolio_info = response.json()
print(portfolio_info)

# test account info 
req_account_info_url = "https://api.skynetsystems.co.th/api/v1/account/000/"+account_no

response = requests.get(req_account_info_url, headers=headers) 
account_info = response.json()
print(account_info)

# test place order 
endpoint = 'https://api.skynetsystems.co.th//api/v1/placeOrder/000'
data = {}
data['accountNo'] = "1053038-1"
data['symbol'] = 'AOT'
data['volume'] = 100
data['position'] = 'O'
data['side'] = 'LONG'
data['price'] = 0
data['priceType'] = 'MP-MKT'
print(data)
json_data = json.dumps(data)

response = requests.post(url = endpoint, headers=headers, data=json_data)
ord_response = response.json()
print(json.dumps(response.json(), indent=4))



# test order info 
req_order_info_url = "https://api.skynetsystems.co.th/api/v1/order/000/"+account_no
res_order_info = requests.get(req_order_info_url, headers=headers) 
order_info = res_order_info.json()
print(order_info)

# test historical candle strick data
symbol = "PTT"
timeframe = "60" #["1","5","15","60","D"]
start_time = "2018-08-17"
end_time = "2018-08-31"
req_hist_data_url = "https://api.skynetsystems.co.th/api/v1/data/candlestick/000/"+account_no+"?symbol="+symbol+"&timeframe="+timeframe+"&startTime="+start_time+"&endTime="+end_time

respones_hist = requests.get(req_hist_data_url, headers=headers)
hist = respones_hist.text

dataframe = pd.read_csv(StringIO(respones_hist.text),
                        names=['time', 'open', 'high', 'low', 'close', 'volume', 'oi'],
                        index_col='time', parse_dates=True)

# test realtime data
"""     
# for realtime.tradeevent
def on_message(channel, method_frame, header_frame, body):
    json_body = json.loads(body)
    print("symbol {}, price {}".format(json_body['symbol'], json_body['price']))
"""
# for realtime.bidoffer
def on_message(channel, method_frame, header_frame, body):
    json_body = json.loads(body) 
    print(json_body)

symbol = "TRUE"

credentials = pika.PlainCredentials('X-API-KEY:4269B42F4E5B1431FC58801B1066FE47', '1053038-1')
parameter = pika.ConnectionParameters(host='data.skynetsystems.co.th', credentials=credentials)
connection = pika.BlockingConnection(parameter)
channel = connection.channel()

result = channel.queue_declare(exclusive=True,  auto_delete=True)
queue_name = result.method.queue
#binding_key = "realtime.tradeevent." + symbol   #realtime.bidoffer.symbol
binding_key = "realtime.bidoffer." + symbol 
channel.queue_bind(exchange='amq.topic', queue=queue_name, routing_key=binding_key)
channel.basic_consume(on_message, queue_name, no_ack=True)

try:
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
connection.close()