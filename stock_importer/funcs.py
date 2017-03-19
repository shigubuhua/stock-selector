#!/usr/bin/python3
# -*- coding: utf-8 -*-

import datetime
import models
import easyquotation

#for fbprophet simple predictor
import pandas as pd
import numpy as np
from fbprophet import Prophet

#not used method
def genCoredata(rawdata):    #strip off useless data and output only needed data
    # dateTime = rawdata.get('datetime')
    # code = rawdata.get('code')
    # name = rawdata.get('name')
    # volume = rawdata.get('volume') #交易金额
    # now = rawdata.get('now')  #现价
    # high = rawdata.get('high')
    # low = rawdata.get('low')
    # open = rawdata.get('open')
    # close = rawdata.get('close')
#need rewrite
    items = [
        'datetime',
        'code',
        'name',
        'volume',
        'now',
        'high',
        'low',
        'open',
        'close',
        'turnover'
    ]
    coredata = {}
    for i in items:
        coredata.update({i, rawdata.get(i)})
    return coredata

#task: calculate daily Kline; update Stat; close and clear cache;
def do_daily_update(rawdata):   #this has nothing to do with quoter, only processing data
    if not rawdata == None:
        return False
    for i in rawdata:
        stock = rawdata.get(i)
        bStock = models.Stock
        bStock.save(stock)
        dailyKline = models.DailyKline(i, bStock)
        dailyKline.save
        
    return True
#task: update cache, update stat, update stocklist incase new stock; sorting max, min
def do_hourly_update(rawdata):
    #generate hourly Kline
    return True
#task: only check code of tracking list;
def do_minute_update():
    trackings = []
    #TODO: query tracking list and exe tradecommand;
    quo = easyquotation.use('qq')
    res = quo.stocks(trackings)
    for i in res:
        stock_update(res.get(i))
#        stock_trad(res.get(i))
    return True

def stock_update(stock):
    #refresh cache, 
    #do trade
    return None