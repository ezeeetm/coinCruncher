#!/usr/bin/env python
import time
import requests
import json
from time import sleep

refresh_local = True            # True | False
currency_source = 'api'      # 'local' | 'api'
chart_history_source = 'local'  # 'local' | 'api'
parse_periods = ['1d']            # ['1d','4h','2h','30m','15m','5m']

periods = {
    '5m' : {'seconds': 300, 'chart_history':{}},
    '15m' : {'seconds': 900, 'chart_history':{}},
    '30m' : {'seconds': 1800, 'chart_history':{}},
    '2h' : {'seconds': 7200,  'chart_history':{}},
    '4h' : {'seconds': 14400, 'chart_history':{}},
    '1d' : {'seconds': 86400, 'chart_history':{}},
}

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

        request_timer = time.time()
        resp = requests.get( url )
        request_timer_elapsed = (time.time() - request_timer)

        # Please note that making more than 6 calls per second to the public API, or repeatedly and needlessly fetching excessive amounts of data, can result in your IP being banned
        if request_timer_elapsed < .17:
            sleep(.17-request_timer_elapsed)

        if 'error' in resp.text:
            raw_currency_list.pop(currency, None)
            print "%s %s %s" % ( len(raw_currency_list), currency, resp.text)

    return raw_currency_list

def chart_history_factory ( currency_list ):
    for period in parse_periods:
        print "---PERIOD: %s ---" % (period)
        for currency in currency_list:
            print "---CURRENCY: %s ---" % (currency)
            url = "https://poloniex.com/public?command=returnChartData&currencyPair=BTC_%s&start=1497135045&end=9999999999&period=%s" % ( currency, periods[period]['seconds'] )

            request_timer = time.time()
            resp = requests.get( url )

            request_timer_elapsed = (time.time() - request_timer)

            # Please note that making more than 6 calls per second to the public API, or repeatedly and needlessly fetching excessive amounts of data, can result in your IP being banned
            if request_timer_elapsed < .17:
                sleep(.17-request_timer_elapsed)

            print resp.json()
            periods[period]['chart_history'][currency]= resp.json()
            print periods

    return periods

if __name__ == '__main__':
    start_time = time.time()

    if currency_source == 'api':
        raw_currency_list = get_raw_currency_list()
        currency_list = scrub_raw_currency_list( raw_currency_list )

    #if currency_source == 'local':
        #currency_list = read from disk

    periods_with_chart_histories = chart_history_factory( currency_list )

    elapsedTime = (time.time() - start_time)/60
    print "---finished in %s minutes ---" % (elapsedTime)