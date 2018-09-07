import requests 
import config 
import json 

class SkynetPortfolio:
    def __init__(self):
        self.header = {"X-API-KEY": config.api_key}
        self.account_no = config.account_no
        
    def req_portfolio_info(self, account_no=config.account_no):
        url = "https://api.skynetsystems.co.th/api/v1/portfolio/000/" + account_no
        r = requests.get(url, headers=self.header)
        return r.json()

    def req_account_info(self, account_no=config.account_no):
        url = "https://api.skynetsystems.co.th/api/v1/account/000/" + account_no
        r = requests.get(url, headers=self.header)
        return r.json()
