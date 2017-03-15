#!/usr/bin/python3
# -*- coding: utf-8 -*-

import datetime
import models

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

def do_daily_update(rawdata):   #this has nothing to do with quoter, only processing data

    return None

def do_hourly_update(rawdata):

    return None

def do_minute_update(rawdata):

    return None
