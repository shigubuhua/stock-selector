#!/usr/bin/python3
# -*- coding: utf-8 -*-
import datetime
import re
import json
from pymongo import MongoClient
import tushare as ts
#we use utc+8 timezone time; makesure env has right configured!
#client = MongoClient()
#db = client.stock_normal
def donothing():
    return None

    
class Base:
    client = MongoClient()
    db = client.stock_normal   #TO CHECK: whether only one instance for many objecst inheritated;
    source = 'normal'
    def changeSource(self, target):
        if target == 'normal':
            db = client.stock_normal
            self.source = target
        elif target == 'test':
            db = client.stock_test
            self.source = target
        else:
            raise ValueError('wrong target input')
    
    def validateSource(self):
        return self.source
    #def save(self):
        #print('save'), to be override;
    #    return None

class Stat(Base):
    col = Base.db.stat
    #a config collection. has many system status; this list all keys names;
    items = [
        'stock_count', #all count of the stock list, all/active/
        'started_datetime', #the initial scripting TimeoutError
        'lastquery_datetime', # the last datetime of data query
        'lastvisit_datetime', # the last change from user or owner
        #'stock_list',    #a list of all stock code#deprecate
        'stock_stat',    #a dict of all stock code and its state code: active or other
    ]
    def __init__(self):
        donothing()
        #init the class, reserved method;
        self.param = {}
        #
        #
        self.load
    def load(self):
        #load all var from db, if not exist, use all value;
        #
        for i in self.items:
            value = self.col.find_one({'key': i})
            self.param.update({i, value})


    def update(self, rawdata):
        #update the current data to db for each ObjID
        #check stock_list

        #update value and save all changed key values;
        return None

#the daily item for each stock
class StockDaily(Base):
    col = Base.db.stockdaily
    source = ts
    def save_by_input(self, stock):
        #directly input buy given dict;
        return self.col.instert_one(stock).inserted_id
    
    def find_by_code(self, code):
        #find code's history, translate
        return  self.col.find({"code": code}).sort("datetime")    #TODO: this returns cursor not objs;

    def find_by_date(self, date):
        #find daily all stocks for specific date
        res = self.col.find({"date": date}).sort("code")

    def import_from_ts(self, code):
        #resolve code(sh , sz pattern) and save all records, item by item, reject duplicated save;
        res = ts.get_hist_data(code)
        #to json and factory new data
        obj = json.loads(res.to_json(orient='index'))  #only this format suits
        for i in obj:
            dateTime = datetime.datetime.strptime(i +" 15:00", "%Y-%m-%d %H:%M")   #2011-12-20, plus 15:00:00 use format;
            dateD = dateTime.date()
            stockdict = obj.get(i)
            stockdict.update({'code': code, 'date': dateD})
            self.col.insert_one(stockdict).inserted_id         
        
    def update_today(self):
        #save the queryed item,
        res = ts.get_today_all()
        obj = json.loads(res.to_json(orient='index'))
        dateD = datetime.datetime.now()
        # if dateD.timetuple[3] == 9 & dateD.timetuple[4] >= 30:
        #     res = ts.get_today_all()
        # elif dateD.timetuple[3] > 9 :
        #     res = ts.get_today_all()
        # elif dateD.timetuple[3] < 9:
        ds = 3600*(dateD.timetuple()[3]+1)
        dt = datetime.timedelta(seconds=ds)
        dateD = dateD -  dt
           
        counting = 0
        for i in obj:
            #dateTime = datetime.datetime.strptime(i, "%Y-%m-%d")
            stock = obj.get(i)
            if self.col.find_one({"date": dateD, "code": stock.get('code')}) == None:
                stock.update({"date": dateD})
                self.col.insert_one(stock).inserted_id
                counting+= 1
        return counting


# code：代码
# name:名称
# changepercent:涨跌幅
# trade:现价
# open:开盘价
# high:最高价
# low:最低价
# settlement:昨日收盘价
# volume:成交量
# turnoverratio:换手率
# amount:成交量
# per:市盈率
# pb:市净率
# mktcap:总市值
# nmc:流通市值


class StockItem(Base):
    col = Base.db.stockindex  #a stock index collection
    def append(self, code):
        donothing() # append to stat all;
    def stop(self, code):
        #ting pai
        return None

    def reopen(self, code):
        #fu pai
        return None

    def change(self, code):
        # do sth like fuquan, zeng fa, etc;
        return None

#class for hourly Kline
class HourKline(Base):
    col = Base.db.hourkline
    items= [
        'high',   #in cent(100 = 1 Yuan)
        'low',
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

        return None

#class for daily Kline
class DailyKline(Base):
    items = [
        'high',   #in cent(100 = 1 Yuan) ??? not sure
        'low',
        'open',
        'now',
        'close',
        'code',
        'turnover',
        'volume',
        'datetime']
    col = Base.db.dailykline
    
    def __init__(self, code, stock):
        #for daily total klines;
        self.stock = stock
        self.code = code
        
    def save(self):
        dailykline = {
            'datetime': self.stock.get('datetime'),
            'code': self.code,
            'open': self.stock.get('open'),
            'now': self.stock.get('now'),
            'high': self.stock.get('high'),
            'low': self.stock.get('low'),
            # 'volume': self.stock.get('volume'),
            'volpercent': self.stock.get('volume') / float(self.stock.get('流通市值'))   #to check!
        }
        return self.col.insert_one(dailykline).inserted_id

#class for trade command formats and records, seemly useless
class TradeCommand(Base):
    col = Base.db.tradecommand
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

#class for owned stocks
class OwnedStock(Base):
    col = Base.db.ownedstock
    def __init__(self, acc, code, hands):
        #the price depend on market
        self.acc = acc
        self.code = code
        self.hands = hands
    # def save(self):
    
    # def sell(self):
    
    # def checkprice(self):

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
    col = Base.db.trade
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
    col = Base.db.account
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

    # def addTrade(self, tradeCommand):
        #add a command to this account
        #         
    # def checkTrade(self):
        #return a list of added tradecommand ( include history )

    # def sell(self, code, hands, price):
        #if owned this code, sell the with a given price and add balance

    # def buy(self, code, hands, price):
        #if balance can afford, decrease balance, add or increase owned stock code and hands and price
        
    # def checkOwned(self):
        #return a list of code and hands;

    # def update(self):
        #save this object; before commit must find this obj;
