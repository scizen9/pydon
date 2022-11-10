#!/kroot/rel/default/bin/kpython

import ktl
import time
import sys
from datetime import datetime, timedelta

tthresh = -100.     # Temperature threshhold

timestr = time.strftime("%Y-%m-%d %H:%M:%S")
n_minutes_ago = datetime.now() - timedelta(minutes=15)

verbose = len(sys.argv) > 1

try:
    ktl_temperature = ktl.cache('krds', 'tempdet')
except:
    if verbose:
        print(timestr + ': KRDS server not running!')
    sys.exit(0)

temperature = float(ktl_temperature.read())
# Pressure exceeds threshhold
if temperature > tthresh:
    print(timestr + ": Temperature exceeds %.1f: %.1f" % (tthresh, temperature))
else:
    if verbose:
        print(timestr + ": Temperature is %.1f" % temperature)
