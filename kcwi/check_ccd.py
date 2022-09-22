#!/kroot/rel/default/bin/kpython

import ktl
import time
import os
import sys
from datetime import datetime, timedelta

timestr = time.strftime("%Y-%m-%d %H:%M:%S")
n_minutes_ago = datetime.now() - timedelta(minutes=15)

verbose = len(sys.argv) > 1

try:
    ktl_ccdpower = ktl.cache('krds', 'CCDPOWER')
except ktl.Exceptions.ktlError:
    if verbose:
        print(timestr + ': KRDS server not running!')
    sys.exit(0)

ccdpower = int(ktl_ccdpower.read())
# power is on
if ccdpower == 1:
    # check last file
    ktl_loutfile = ktl.cache('krds', 'LOUTFILE')
    loutfile = ktl_loutfile.read()
    # loutfile is set
    if len(loutfile.strip()) > 0:
        ts = os.path.getmtime(loutfile)
        ftime = datetime.fromtimestamp(ts)

        if ftime < n_minutes_ago:
            print(timestr + ": CCDPOWER ON!")
            print("Last file at " + ftime.strftime('%Y-%m-%d %H:%M:%S')
                  + ": " + loutfile)
        else:
            if verbose:
                print(timestr + ": CCDPOWER ON!")
                print("Last file at " + ftime.strftime('%Y-%m-%d %H:%M:%S')
                      + ": " + loutfile)
    else:
        print(timestr + ": CCDPWER ON!")
        print("Last file not recorded by server")
else:
    if verbose:
        print(timestr + ": CCDPOWER OFF")
