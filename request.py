#!/usr/bin/env python
import requests
import json
import time
from time import sleep
import sys

retry_threshold = 5
api_throttle = .2 # Please note that making more than 6 calls per second to the public API, or repeatedly and needlessly fetching excessive amounts of data, can result in your IP being banned


def request(url):
    retry = 1
    while retry <= retry_threshold:
        try:
            request_timer = time.time()
            resp = requests.get(url)
            return json.loads(resp.text)

        except:
            print "WARN: requesting %s failed on retry %s" % ( url, retry )
            retry += 1
            request_timer_elapsed = (time.time() - request_timer)
            if request_timer_elapsed < api_throttle:
                sleep(api_throttle-request_timer_elapsed)
                
    print "FATAL: requesting %s failed after %s retries" % ( url, retry_threshold )
    sys.exit()