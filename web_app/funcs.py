#!/usr/bin/python3
# -*- coding: utf-8 -*-
#ganben stock web functions part
import datetime
import re
import json

#if posted code is valid; improve: if code existed in db.stockindex
def valid_code(vcode):
    if re.match('\d{6}', vcode):
        return True
    else:
        return False

