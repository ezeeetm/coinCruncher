#!/usr/bin/env python
import time
from request import request
from local_data import *

parent_currencies = [
    'BTC',
    'ETH',
    'XMR',
    'USDT'
]


def get_currencies():
    currencies = request('https://poloniex.com/public?command=returnCurrencies')
    for currency in currencies.keys():
        if currencies[currency]['delisted'] == 1:
            currencies.pop(currency, None)
            print "%s delisted" % ( currency )
            continue
    return currencies


def currency_pair_factory(currencies):
    print '### Adding Currency Pairs ###'
    currency_pairs = []
    for parent_currency in parent_currencies:
        for currency in currencies:
            cpair_string = "%s_%s" % (parent_currency, currency)
            test_url = "https://poloniex.com/public?command=returnChartData&currencyPair=%s&start=0000000000&end=9999999999&period=%s" % ( cpair_string, 86400 )

            test_resp = request(test_url)

            if 'error' not in test_resp:
                print "      %s" % (cpair_string)
                currency_pairs.append(cpair_string)
    write ('.\data\currency_pairs.json', currency_pairs )

if __name__ == '__main__':
    start_time = time.time()
    currencies = get_currencies()
    currency_pair_factory(currencies)