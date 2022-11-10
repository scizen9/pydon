#!/kroot/rel/default/bin/kpython

import ktl
import time
import sys
from datetime import datetime, timedelta

pthresh = 1.e-6     # Pressure threshhold

timestr = time.strftime("%Y-%m-%d %H:%M:%S")
n_minutes_ago = datetime.now() - timedelta(minutes=15)

verbose = len(sys.argv) > 1

try:
    ktl_pressure = ktl.cache('krvs', 'pressure')
except ktl.Exceptions.ktlError:
    if verbose:
        print(timestr + ': KRVS server not running!')
    sys.exit(0)

pressure = int(ktl_pressure.read())
# Pressure exceeds threshhold
if pressure > pthresh:
    print(timestr + ": Pressure exceeds %.3e: %.3e" % (pthresh, pressure))
else:
    if verbose:
        print(timestr + ": Pressure is %.3e" % pressure)
