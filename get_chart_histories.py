#!/usr/bin/env python
import time
from request_helper import request
from data_helper import *


parse_periods = ['1d','4h','2h','30m','15m','5m']  # ['1d','4h','2h','30m','15m','5m']
periods = {
    '5m' : {'seconds': 300 },
    '15m' : {'seconds': 900 },
    '30m' : {'seconds': 1800 },
    '2h' : {'seconds': 7200 },
    '4h' : {'seconds': 14400 },
    '1d' : {'seconds': 86400 }
}

def get_currency_pairs():
    currency_pairs = read('.\data\currency_pairs.json')
    return currency_pairs

def chart_history_factory ( currency_pairs ):
    for period in parse_periods:
        print "---PERIOD: %s ---" % (period)
        for currency_pair in currency_pairs:
            print "     --- CURRENCY PAIR: %s ---" % (currency_pair)
            url = "https://poloniex.com/public?command=returnChartData&currencyPair=%s&start=0000000000&end=9999999999&period=%s" % ( currency_pair, periods[period]['seconds'] )
            chart_history = request ( url )
            for record in chart_history:
                record.pop("quoteVolume", None)
                record.pop("high", None)
                record.pop("low", None)
                record.pop("close", None)
                record.pop("open", None)
            file = ".\data\chart_histories\%s\%s.json" % (period, currency_pair)
            write (file, chart_history)


if __name__ == '__main__':
    start_time = time.time()
    currency_pairs = get_currency_pairs()
    chart_history_factory ( currency_pairs )
    elapsedTime = (time.time() - start_time)/60
    print " ---finished in %s minutes ---" % (elapsedTime)