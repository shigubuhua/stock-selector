#!/usr/bin/python3
# -*- coding: utf-8 -*-
#ganben for fracegan stock selector, stock information importer

import pymongo
import time, threading, datetime
from queue import Queue
from functools import lru_cache
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
tracking_list = db.tracking_list    #provide tracking 1min tick data;
jobque = Queue.Queue(40)

lastUpdateDatetime = datetime.datetime.strptime("17-03-03-15-50", "%y-%m-%d-%H-%M")
lastUpdateDatetimeTuple = lastUpdateDatetime.timetuple() #,init date time time0=year 1=month, 2=day, 3 = hour, 4= minuete 6 = days of week
switch = False
queueLock = threading.Lock()

#@lru_cache(maxsize=32)  #notsure if need cache tools
def updateLastTimeTuple():
    global lastUpdateDatetime, lastUpdateDatetimeTuple
    #global var update need declaration
    present = datetime.datetime.now()
    lastUpdateDatetime = present
    lastUpdateDatetimeTuple = present.timetuple()

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
class WorkerThreading(threading.Thread):
    def __init__(self, q):
        threading.Thread.__init__(self)
        self.q = q
#        self.threadID = threadID

    def run(self):
        global switch
        #this variable is needed to declaration for modify

        while not restart_flag:
#            queueLock.acquire()
# everyday, 900 1000 1100 1130 1300 1400 1500
            #global var read need no declaration;
            present = datetime.datetime.now()
            presentTimetuple = present.timetuple()   # [0]=year [1]=month [2]=day [3]=hour [4]=min

            #update time
            if not switch:      #if switch off, if a newday(day - last = 1 ), yes then query all at 0900 and switch on;
                if presentTimetuple[2] - lastUpdateDatetimeTuple[2] >= 1 & presentTimetuple[3] == 9:
                    do_daily_update()
                    updateLastTimeTuple()
                    switch = True
            else:
            #if switch on, query all at 0930, find res if updated(work day), else switch off;
                if presentTimetuple[3] == 9 & presentTimetuple[4] == 30 :
                    do_hourly_update()
                    do_switch()
                elif presentTimetuple[3] - lastUpdateDatetimeTuple[3] >= 1 :
                    do_hourly_update()
                elif presentTimetuple[4] - lastUpdateDatetimeTuple[4] >= 1 :
                    do_minute_update()

            #if switch on, query all at 0930 1030 1130 1300 1400 1500 for hourly Kline;
            #if switch on but not triggered above, update tracking list every minute; (min - min > 1)
            #if > 1530, switch off;
            #every query 沉睡54s
            time.sleep(54)

#only exe as main
#maintain timer tag and worker threading
if __name__ == "__main__":
    #do main method;
    try:
        init()  #start worker thread

    except:
        exit()
    # while True: if the que not empty, the worker thread is kill, restart worker thread