#!/usr/bin/python3
# -*- coding: utf-8 -*-
#ganben for fracegan stock study, web interface

from flask import Flask, url_for    #for static and url building
from ..stock_importer import models   #for stock obj and data
from flask import render_template     #for template rendering
from flask import request  #for http method(api ?)
from .funcs import *     #for all need functions

app = Flask(__name__)
url_for('static', filename='style.css')


@app.route('/')
def index_hello():
    return 'This is index, hello!'

@app.route('/stock/<string:stock>')
def stock_information(stock):
    #TODO: render_template(a html) prepare stock item 2W day k-line
    return 'stock name is %s' % stock

@app.route('/observing')
@app.route('/observing/<int:ob_id>')
def observings(ob_id=None):
    #resolve template and static files
    #prepare data: 2week daily Kline for observing list;
    return 'this is a observing list'

@app.route('/results/<int:res_id>')
def results(res_id=None):
    #store the observing strategy results
    return 'this is some results'

@app.route('/api/obs/<command>', methods=['GET', 'POST'])
def api_obs(command):
    #TODO: return the observed data
    error = None
    stock = models.StockItem()
    if request.method == 'POST' and command == 'add':
        if valid_code(request.form['code']):

            return stock.add_observe(request.form['code'])
        else:
            error = 'Invalid code'
        return render_template('observe.html', error = error)
    elif request.method == 'POST' and command == 'del':
        if valid_code(request.form['code']):
            #.get_observe()    #find by code;
            stock.delete_observe(request.form['code'])
        else:
            error = 'Invalid code'
        return render_template('observe.html', error = error)
    elif request.method == 'GET' and command == 'all':
        b = stock.get_observe()
        return b
    elif request.method == 'GET' and re.match('\d{6}', command):
        b = stock.get_observe()
        return b.index(command)
    else:
        return 'unsupported input'

@app.route('/api/strategy/<command>', methods=['GET', 'POST'])
def api_strategy(command):
    #command = add update new of code/account
    if request.method == 'POST' and command == 'add':
        return None
