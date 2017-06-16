#!/usr/bin/env python
import json
import os
import errno

def write (file, data):
    if not os.path.exists(os.path.dirname(file)):
        try:
            os.makedirs(os.path.dirname(file))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    with open(file, 'w') as outfile:
        json.dump(data, outfile)