import requests 
import config 
import json 
class SkynetOrder:
    def __init__(self):
        self.order_header = {'Content-Type' : 'application/json', 'X-API-KEY': config.api_key}
        self.place_order_url = "https://api.skynetsystems.co.th/api/v1/placeOrder/000"
    
    def place_order(self, symbol, action, volume, order_type="MP", price=0, account_no=config.account_no):
        order_pack = {}
        order_pack['accountNo'] = account_no
        order_pack['symbol'] = symbol
        order_pack['volume'] = volume

        if action == "Buy" or action == "buy" :     
            order_pack['position'] = 'O'
            order_pack['side'] = 'LONG'
        elif action == "Sell" or action == "sell":
            order_pack['position'] = 'C'
            order_pack['side'] = 'SHORT'
        else : 
            print("Action can be only Buy/Sell")

        order_pack['price'] = price
        order_pack['priceType'] = order_type
        json_data = json.dumps(order_pack)

        response = requests.post(url = self.place_order_url, headers=self.order_header, data=json_data)
        ord_response = response.json()
        return ord_response