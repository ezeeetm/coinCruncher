#!/usr/bin/env python

import requests
import json
import os
import errno
import time
import shutil

periods = [ 
    {'seconds': 300, 'friendlyName': '5m'},
    {'seconds': 900, 'friendlyName': '15m'},
    {'seconds': 1800, 'friendlyName': '30m'},
    {'seconds': 7200, 'friendlyName': '2h'},
    {'seconds': 14400, 'friendlyName': '4h'},
    {'seconds': 86400, 'friendlyName': '1d'}
]

def get_currency_list():
    resp = requests.get('https://poloniex.com/public?command=returnCurrencies')
    currencies_json = json.loads(resp.text)
    return currencies_json

def parse_currencies( currency_list ):
    for currency in currency_list.keys():
        
        if currency_list[currency]['delisted'] == 1:
            currency_list.pop(currency, None)
            print "%s delisted" % ( currency )
            continue

        for period in periods:

            url = "https://poloniex.com/public?command=returnChartData&currencyPair=BTC_%s&start=0000000000&end=9999999999&period=%s" % ( currency, period['seconds'] )

            resp = requests.get( url )

            if 'error' in resp.text:
                currency_list.pop(currency, None)
                print "%s %s %s" % ( len(currency_list), currency, resp.text)
                break

            filename = ".\currencies\%s\%s.json" % ( currency, period['friendlyName'] )
            if not os.path.exists(os.path.dirname(filename)):
                try:
                    os.makedirs(os.path.dirname(filename))
                except OSError as exc: # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise

            with open(filename, "w") as f:
                f.write(resp.text)

    with open('.\currencies\_currencies.json', 'w') as f:   
        json.dump(currency_list, f, sort_keys=True, indent=4, separators=(',', ': '))

    


if __name__ == '__main__':
    start_time = time.time()
    if os.path.isdir('.\currencies'):
        shutil.rmtree('.\currencies')
    currency_list = get_currency_list()
    parse_currencies( currency_list )
    elapsedTime = (time.time() - start_time)/60
    print "---finished in %s minutes ---" % (elapsedTime)