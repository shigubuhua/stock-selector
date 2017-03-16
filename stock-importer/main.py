#!/usr/bin/python3
# -*- coding: utf-8 -*-
#ganben for fracegan stock selector, stock information importer

import logging
import pymongo
import time, threading, datetime
from queue import Queue
from functools import lru_cache
from pymongo import MongoClient
import easyquotation
#import other function and packages in this folders
import models
import funcs

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
logging.basicConfig(filename = 'mainquoter.log', level = logging.INFO)
logger = logging.getLogger('__main__')

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
jobque = Queue(40)

lastUpdateDatetime = datetime.datetime.strptime("17-03-03-15-50", "%y-%m-%d-%H-%M") #should read from db.stat key=lastUpdateTime
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

def reinit():
    #start a checker, provide hourly and daily checker for proper attemp.
    global quo
    global client
    global restart_flag
    global db
    quo = easyquotation.use('qq')
    client = MongoClient()         #probably move into models module or funcs module!
    db = client.stock_normal
    restart_flag = 0

def query_all():
    global restart_flag

    try:
        #time = #the time
        res = quo.all_market
        stocklistNew = []
        coredata = {}
        for e in res:
            stocklistNew.append(e)
        #compare if new stock -> only daily change;
        for i in stocklistNew:
            stockDetail = res.get(i)
            #db.stock_all.insert_one(stockDetail)   #not save here
            coredata.update({i, funcs.genCoredata(res.get(i))})
            #append data to all
            #this e trigger all the data flow!
    except:
        restart_flag = 1    #if network error occurs, restart thread or re-init instance of db and quoter
        return False
    #return coredata dicts or rawdata? should cache this maybe!
    return coredata   

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
            delta_time = present - lastUpdateDatetime
            #update time
            if not switch:      #if switch off, if a newday(day - last = 1 ), yes then query all at 0900 and switch on;
            # use timedelta instead    if presentTimetuple[2] - lastUpdateDatetimeTuple[2] >= 1 & presentTimetuple[3] == 9:
                if delta_time.days > 0 & presentTimetuple[3] == 9 & presentTimetuple[4] == 30: #switch on if daily 0930
                    fresh = query_all
                    #TODO: if fresh data is active then switch on, other wise just updateLastTimeTuple

                    funcs.do_hourly_update(fresh)
                    updateLastTimeTuple()
                    switch = True
            else:
            #if switch on, query all at 0930, find res if updated(work day), else switch off;
                #if presentTimetuple[3] == 9 & presentTimetuple[4] == 30 :
                #    do_hourly_update()
                #    do_switch()
                #    updateLastTimeTuple()
                if presentTimetuple[3] == 15 :     #close if after 1500
                    fresh = query_all
                    funcs.do_daily_update(fresh)
                    updateLastTimeTuple()
                    switch = False
                elif delta_time.seconds >= 3600 & delta_time.seconds < 7200 :  #do between 1h to 2h
                    fresh = query_all
                    if funcs.do_hourly_update(fresh):
                        updateLastTimeTuple()
                elif delta_time.seconds >= 60 & delta_time.seconds < 100:  #do between 60s and 100s
                    #TODO: only query tracking list datas; 
                    #get code list
                    #query result
                    if funcs.do_minute_update(fresh):
                        updateLastTimeTuple()

            #if switch on, query all at 0930 1030 1130 1300 1400 1500 for hourly Kline;
            #if switch on but not triggered above, update tracking list every minute; (min - min > 1)
            #if > 1530, switch off;
            #every query 沉睡54s
            time.sleep(45)


def donothing():
    global logger
    logger.info('donothing')

#only exe as main
#maintain timer tag and worker threading
if __name__ == "__main__":
    #TODO: do main method; a thread always open threading and reinit this threading!
    try:
        #start worker thread and
        timer = WorkerThreading(jobque)
        timer.start()
    except:
        #raise Exception('main exception')
        timer.join()
        reinit()        
    # while True: if the que not empty, the worker thread is kill, restart worker thread