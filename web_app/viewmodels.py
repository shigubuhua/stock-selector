#!/usr/bin/python3
# -*- coding: utf-8 -*-
#ganben stock web view models part
from .stock_importer.models import *

#index models
def genIndex():
    obs = {}
    title = 'hello word'
    obs.update({"title": title})
    b = OwnedStock()
    stocks = b.findall()
    obs.update({"stocks": stocks})
    return obs
