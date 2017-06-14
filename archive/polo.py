#!/usr/bin/env python

import requests
import json
import os
import errno
import time
import shutil

periods = [ 
    #{'seconds': 300, 'friendlyName': '5m'},
    #{'seconds': 900, 'friendlyName': '15m'},
    #{'seconds': 1800, 'friendlyName': '30m'},
    #{'seconds': 7200, 'friendlyName': '2h'},
    #{'seconds': 14400, 'friendlyName': '4h'},
    {'seconds': 86400, 'friendlyName': '1d'}
]

def get_raw_currency_list():
    resp = requests.get('https://poloniex.com/public?command=returnCurrencies')
    currencies_json = json.loads(resp.text)
    return currencies_json

def scrub_raw_currency_list( raw_currency_list ):
    for currency in raw_currency_list.keys():
        if raw_currency_list[currency]['delisted'] == 1:
            raw_currency_list.pop(currency, None)
            print "%s delisted" % ( currency )
            continue

        url = "https://poloniex.com/public?command=returnChartData&currencyPair=BTC_%s&start=0000000000&end=9999999999&period=%s" % ( currency, 86400 )

        resp = requests.get( url )

        if 'error' in resp.text:
            raw_currency_list.pop(currency, None)
            print "%s %s %s" % ( len(raw_currency_list), currency, resp.text)
    
    return raw_currency_list


def parse_currencies( currency_list ):
    for period in periods:
        period_set = {}
        for currency in currency_list:
            url = "https://poloniex.com/public?command=returnChartData&currencyPair=BTC_%s&start=1497135045&end=9999999999&period=%s" % ( currency, period['seconds'] )

            resp = requests.get( url )
            period_set[currency] = resp.json()

        print period_set
        cont = raw_input()


if __name__ == '__main__':
    start_time = time.time()
    raw_currency_list = get_raw_currency_list()
    currency_list = scrub_raw_currency_list( raw_currency_list )
    parse_currencies( currency_list )
    elapsedTime = (time.time() - start_time)/60
    print "---finished in %s minutes ---" % (elapsedTime)