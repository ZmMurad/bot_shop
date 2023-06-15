import requests as re
from config import *


class CryptoCloud:
    def __init__(self,cost):
        self.cost=cost
        self.url="https://api.cryptocloud.plus/v1/invoice/"
        self.shop_id=shop_id
        self.result=None
        self.response=None
        
    def create_bill(self):
        self.result=re.post(self.url+"create",headers=TOKEN_CRYPTOCLOUD, data={"shop_id":self.shop_id,"amount":self.cost})
        self.result.raise_for_status()
        return self.result.json()["pay_url"]
    
    def check_bill(self):
        self.response=re.get(self.url+"info",headers=TOKEN_CRYPTOCLOUD,params={"uuid":self.result.json()["invoice_id"]})
        self.response.raise_for_status()
        return self.response.json()["status_invoice"]
    
    def get_invoice_id(self):
        return self.result.json()["invoice_id"]

    def return_info_to_db(self) -> list:
        '''Возвращает списко с суммой и ВРЕМЕНИ ОПЛАТЫ В КРИПТОКЛАУД НЕТ, ПОЭТОМУ ДОБАВЛЮ None, для добавления в бд'''
        if self.check_bill()=="paid":
            list_out=[]
            list_out.append(self.cost)
            list_out.append(None)
            return list_out

class CryptoBot:
    def __init__(self,cost) -> None:
        self.cost=cost
        self.result=None
        self.response=None
        self.url=URL_CRYPTO_BOT
        
    def test_method(self):
        self.response=re.post(self.url+"getMe",headers=TOKEN_CRYPTOBOT)
        self.response.raise_for_status()
        return self.response.text
    
    def create_bill(self,asset):
        self.result=re.post(self.url+"createInvoice",headers=TOKEN_CRYPTOBOT, data={"asset":asset,"amount":self.cost})
        self.result.raise_for_status()
        return self.result.json()["result"]["pay_url"]
    
    def check_bill(self):
        invoice_id=self.get_invoice_id()
        self.response = re.get(self.url+"getInvoices", headers=TOKEN_CRYPTOBOT, params={"invoice_ids":invoice_id})
        return self.response.json()["result"]["items"][0]["status"]
    
    def get_invoice_id(self):
        return self.result.json()["result"]["invoice_id"]
    
    def return_info_to_db(self) -> list:
        '''Возвращает списко с суммой и временем оплаты, для добавления в бд'''
        if self.check_status()=="paid":
            list_out=[]
            list_out.append(self.cost)
            list_out.append(self.result.json()["result"]["paid_at"])
            return list_out
        
