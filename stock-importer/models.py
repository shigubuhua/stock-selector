#!/usr/bin/python3
# -*- coding: utf-8 -*-
import datetime
import re
from pymongo import MongoClient
#we use utc+8 timezone time; makesure env has right configured!
#client = MongoClient()
#db = client.stock_normal
def donothing():
    return None

    
class Base():
    client = MongoClient()
    db = client.stock_normal   #TO CHECK: whether only one instance for many objecst inheritated;
    
    #def save(self):
        #print('save'), to be override;
    #    return None

class Stat:
    def init(self):
        donothing()

class StockItem:
    def append(self):
        donothing() # append to stat all;

#class for hourly Kline
class HourKline(Base):
    items= [
        'max',   #in cent(100 = 1 Yuan)
        'min',
        'open',
        'now',
        'close',
        'code',
        'turnover',
        'volume']
    def __init__(self, code, rawdata_0, rawdata_1):   #rawdata 0:(last hour),1:(current price)
        self.code = code
        self.param_0 = {}     #use instance var to store
        self.param_1 = {}
        for i in self.items:
            self.param_0.update(i, rawdata_0.get(i))
            self.param_1.update(i, rawdata_1.get(i))
    def save(self):

#class for daily Kline
class DailyKline(Base):
    items = [
        'max',   #in cent(100 = 1 Yuan) ??? not sure
        'min',
        'open',
        'now',
        'close',
        'code',
        'turnover',
        'volume',
        'datetime'
    ]
    def __init__(self, rawdata):
        #for daily total klines;
    def save(self):


#class for trade command formats and records, seemly useless
class TradeCommand(Base):
    def __init__(self, cmd, price, hands, code, dt, cplt):
        if cmd == 'buy' or cmd == 'sell':
            self.cmd = cmd
        else:
            raise ValueError('invalid cmd, should be buy or sell') 
        
        if type(price) is float:
            self.price = price
        else:
            raise ValueError('invalid price type, shoud be float')

        if re.match('s[zh]\d{6}', code):      #check if code match quo from qq, [sz]\d6
            self.code = code
        else:
            raise ValueError('invalide code format like sz000000 or sh000000')
        #TODO: complete other variables 
#        self.rawdata = rawdata
    
    def tradecheck(self, rawdata):
        code = self.code
        if self.cmd == 'buy':
            if rawdata.get(code).get('now') == self.price:   #use now price as get traded price
                return True
    

#class for trade action
class Trade(Base):
    items = [
        'cmd',   # buy or sell for whole command content
        'price',  #setted prices
        'hands',   #wanted hands
        'code',     # stock code
        'datetime', #valide before this time
        'complete'    #completed hands 
    ]

    def __init__(self, acc, command):   #command.code price buy/sell timeout
        self.acc = acc
        self.command = {}
        self.complete = 0
        for e in self.items:
            if not command.get(e, 'x') == 'x' : 
                self.command.update(e, command.get(e))    #check command format;
            else:
                raise ValueError

    def check_trade(self, rawdata):
        code = self.command.get('code')
        if rawdata.get(code):
            if rawdata.get(code).get('now') == self.command.get('price'):
                self.complete = 1
                return self.complete
        else:
            return False


#class for 
class Account(Base):
    col = self.db.account
    def __init__(self, acc, balance):    #acc account id, balance in number in yuan
        if re.match('\d{6}', acc):
            self.opening = balance
            self.balance = balance
            self.acc = acc
        else:
            raise ValueError('acc must be six digit')
        
    def save(self):
        if self.col.find_one({'acc': self.acc}):  #check whether unique acc in six digit number
            raise ValueError('duplicated acc')
        account = {'acc': self.acc, 'balance': self.balance}     #need more data, tags etc.
        return self.col.insert_one(account).inserted_id()
    
    def find(self, acc):
        if re.match('\d{6}', acc):
            return self.col.find_one({'acc': acc})
        else:
            raise ValueError('acc must be 6 digit and valid')

    def addTrade(self, tradeCommand):
        #add a command to this account
        #         
    def checkTrade(self):
        #return a list of added tradecommand ( include history )

    def sell(self, code, hands, price):
        #if owned this code, sell the with a given price and add balance

    def buy(self, code, hands, price):
        #if balance can afford, decrease balance, add or increase owned stock code and hands and price
        
    def checkOwned(self):
        #return a list of code and hands;

    def update(self):
        #save this object; before commit must find this obj;
        