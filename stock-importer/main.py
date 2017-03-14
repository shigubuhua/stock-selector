#!/usr/bin/python3
# -*- coding: utf-8 -*-
#ganben for fracegan stock selector, stock information importer

import pymongo
import time, threading
from queue import Queue
from pymongo import MongoClient
import easyquotation
#import other function and packages in this folders


#SW DESIGN:
#job conducting:
#check if today is working day (trading day, or simply everyday compute and daily data auditing)
#daily: 9am -- 15pm querying one time all data and updating to per hour data col.
#daily: end, after 15pm querying all data and append to per day data col
#minute ticking data for trading list and complete trading job;
#calculating real time balancing for accounts/ strategys;
quo = easyquotation.use('qq')
client = MongoClient()
restart_flag = 0
started_flag = 0
#define for standard DBs for data oganization

db = client.stock_normal
# #DB design:
# db.stat -> statistics for each code
# .tags -> tags for each code
# .last -> lastday hourly live data for newsest data
# .stock_all  every recode append
# .stock_day   daily append
# .command basic config like total_list : a dict with all code in list;
# .trade_job :trading for
#detail defined in models.py
stock_all = db.stock_all
stock_day = db.stock_day
last = db.last
trade_job = db.trade_job
jobque = Queue.Queue(100)
lastwork = time.time()     #0=year 1=month, 2=day, 3 = hour, 4= minuete 6 = days of week

def init():
    #start a checker, provide hourly and daily checker for proper attemp.
    #

def query_all():
    try:
        time = #the time
        res = quo.all_market

        for e in res:
            #append data to all
            stock_all.insert_one(e)
            #this e trigger all the data flow!
    except:

        restart_flag = 1


# threadings
class HourlyThreading(threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.q = q
        self.name = name
        self.threadID = threadID

    def run(self):

        while True:



#only exe as main
if __name__ == "__main__":
    #do main method;
    try:
        init()  #start worker thread

    except:
        exit()

    # while True: if the que not empty, the worker thread is kill, restart worker thread
