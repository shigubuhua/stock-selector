#!/usr/bin/python3
# -*- coding: utf-8 -*-
#ganben stock web view models part
from .stock_importer.models import *

#index models
def genIndex():
    main = {}
    title = 'hello word'
    main.update({"title": title})
    # b = OwnedStock()
    # stocks = b.findall()
    # obs.update({"stocks": stocks})
    main.update({"results": "this is results string"})
    testdata1 = {"name": "name1", "trade": 12.2, "changepercent": 5.5}
    testdata2 = {"name": "name2", "trade": 56.5, "changepercent": -2.2}
    stocks = [testdata1, testdata2]
    main.update({"stocks": stocks})
    return main

